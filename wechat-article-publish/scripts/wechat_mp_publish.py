#!/usr/bin/env python3
"""Create and publish WeChat Official Account drafts from local article files."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any


API_BASE = "https://api.weixin.qq.com"
DEVELOPER_PLATFORM_URL = "https://developers.weixin.qq.com/platform"
INLINE_IMAGE_LIMIT = 1024 * 1024
DEFAULT_CREDENTIALS_FILE = Path.home() / ".config" / "wechat-mp" / ".env"
IMG_SRC_RE = re.compile(r"(<img\b[^>]*?\bsrc\s*=\s*)([\"'])(.*?)(\2)", re.I | re.S)
PRE_BLOCK_RE = re.compile(r"<pre\b(?P<attrs>[^>]*)>(?P<body>.*?)</pre>", re.I | re.S)
STYLE_ATTR_RE = re.compile(r"\bstyle\s*=\s*([\"'])(?P<style>.*?)\1", re.I | re.S)
CODE_WRAPPER_RE = re.compile(r"^\s*<code\b[^>]*>(?P<body>.*?)</code>\s*$", re.I | re.S)
DEFAULT_CODE_STYLE = (
    "display:block;box-sizing:border-box;max-width:100%;"
    "margin:16px 0 22px;padding:16px;background:#0f172a;color:#dbeafe;"
    "border-radius:8px;word-break:break-all;overflow-wrap:anywhere;"
    "font-size:14px;line-height:1.75;"
    "font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;"
)


class WeChatError(RuntimeError):
    pass


def developer_platform_hint(message: str) -> str | None:
    normalized = message.lower()
    if "set wechat_access_token" in normalized or "wechat_app_id" in normalized:
        return (
            f"请到 {DEVELOPER_PLATFORM_URL} 获取或核对公众号 AppID/AppSecret，"
            f"再写入 {DEFAULT_CREDENTIALS_FILE}。"
        )
    if "40164" in normalized or "invalid ip" in normalized or "whitelist" in normalized:
        return (
            f"请到 {DEVELOPER_PLATFORM_URL} 的公众号开发配置中，"
            "将当前服务器出口 IP 加入 IP 白名单。"
        )
    if "40001" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 核对 AppID/AppSecret 或 access token 所属账号。"
    if "48001" in normalized or "53504" in normalized or "53505" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 检查接口权限、账号认证状态和发布相关能力。"
    if "wechat api error" in normalized or "wechat http" in normalized:
        return (
            f"如属于公众号配置或权限问题，请到 {DEVELOPER_PLATFORM_URL} "
            "核对开发配置、IP 白名单、接口权限和账号认证状态。"
        )
    return None


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_env_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_credentials_file(path: Path = DEFAULT_CREDENTIALS_FILE) -> dict[str, str]:
    if not path.exists():
        return {}
    if not path.is_file():
        raise WeChatError(f"WeChat credentials path is not a file: {path}")
    credentials: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in {"WECHAT_ACCESS_TOKEN", "WECHAT_APP_ID", "WECHAT_APP_SECRET"}:
            credentials[key] = strip_env_value(value)
    return credentials


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[text.find("\n", end + 1) + 1 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta, body


def simple_markdown_to_html(text: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{html.escape(' '.join(paragraph))}</p>")
            paragraph = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                blocks.append(wechat_code_block_from_text(chr(10).join(code_lines)))
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            continue
        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if image_match:
            flush_paragraph()
            alt, src = image_match.groups()
            blocks.append(f'<p><img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}"></p>')
            continue
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            blocks.append(f"<h{level}>{html.escape(heading_match.group(2))}</h{level}>")
            continue
        paragraph.append(stripped)

    if in_code:
        blocks.append(wechat_code_block_from_text(chr(10).join(code_lines)))
    flush_paragraph()
    return "\n".join(blocks)


def wechat_code_style(pre_attrs: str) -> str:
    match = STYLE_ATTR_RE.search(pre_attrs)
    raw_style = match.group("style") if match else DEFAULT_CODE_STYLE
    declarations: list[str] = []
    seen: set[str] = set()
    for raw_declaration in raw_style.split(";"):
        if ":" not in raw_declaration:
            continue
        prop, value = raw_declaration.split(":", 1)
        prop = prop.strip().lower()
        value = value.strip()
        if not prop or not value or prop == "white-space":
            continue
        declarations.append(f"{prop}:{value}")
        seen.add(prop)
    required = {
        "display": "block",
        "box-sizing": "border-box",
        "max-width": "100%",
        "word-break": "break-all",
        "overflow-wrap": "anywhere",
        "font-family": "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace",
    }
    for prop, value in required.items():
        if prop not in seen:
            declarations.append(f"{prop}:{value}")
    return ";".join(declarations) + ";"


def code_text_to_wechat_html(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    wrapper_match = CODE_WRAPPER_RE.match(value)
    if wrapper_match:
        value = wrapper_match.group("body")
    value = re.sub(r"<[^>]+>", "", value)
    text = html.unescape(value).strip("\n")
    lines = text.splitlines() or [""]
    encoded_lines = []
    for line in lines:
        escaped = html.escape(line, quote=False)
        escaped = escaped.replace("\t", "&nbsp;" * 4).replace(" ", "&nbsp;")
        encoded_lines.append(escaped or "&nbsp;")
    return "<br>".join(encoded_lines)


def wechat_code_block_from_text(value: str) -> str:
    style = html.escape(DEFAULT_CODE_STYLE, quote=True)
    body = code_text_to_wechat_html(html.escape(value))
    return f'<p style="{style}">{body}</p>'


def normalize_wechat_code_blocks(content: str) -> str:
    """Convert <pre> blocks to WeChat-safe explicit line breaks and spaces."""

    def replace(match: re.Match[str]) -> str:
        style = wechat_code_style(match.group("attrs"))
        body = code_text_to_wechat_html(match.group("body"))
        return f'<p style="{html.escape(style, quote=True)}">{body}</p>'

    return PRE_BLOCK_RE.sub(replace, content)


def markdown_to_html(text: str) -> str:
    try:
        import markdown as markdown_lib  # type: ignore
    except Exception:
        return simple_markdown_to_html(text)
    return markdown_lib.markdown(text, extensions=["extra", "sane_lists"])


def html_body(text: str) -> str:
    match = re.search(r"<body\b[^>]*>(.*?)</body>", text, re.I | re.S)
    return match.group(1).strip() if match else text.strip()


def title_from_html(text: str) -> str | None:
    for pattern in (r"<h1\b[^>]*>(.*?)</h1>", r"<title\b[^>]*>(.*?)</title>"):
        match = re.search(pattern, text, re.I | re.S)
        if match:
            title = strip_tags(match.group(1))
            if title:
                return html.unescape(title)
    return None


def load_article(path: Path) -> tuple[dict[str, Any], str]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(read_text(path))
        if "articles" in data:
            if not data["articles"]:
                raise WeChatError("JSON field 'articles' is empty.")
            article = data["articles"][0]
        else:
            article = data
        content = article.get("content") or article.get("html")
        if not content:
            raise WeChatError("JSON article must contain 'content' or 'html'.")
        return dict(article), normalize_wechat_code_blocks(str(content))

    text = read_text(path)
    if suffix in {".html", ".htm"}:
        content = html_body(text)
        meta: dict[str, Any] = {}
        found_title = title_from_html(text)
        if found_title:
            meta["title"] = found_title
        return meta, normalize_wechat_code_blocks(content)

    if suffix in {".md", ".markdown"}:
        meta, body = parse_frontmatter(text)
        if "title" not in meta:
            heading = re.search(r"^#\s+(.+)$", body, re.M)
            if heading:
                meta["title"] = heading.group(1).strip()
        return meta, normalize_wechat_code_blocks(markdown_to_html(body))

    raise WeChatError(f"Unsupported article file type: {suffix}")


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise WeChatError(f"{label} not found: {path}")
    if not path.is_file():
        raise WeChatError(f"{label} is not a file: {path}")


def is_remote_src(src: str) -> bool:
    return src.startswith("http://") or src.startswith("https://")


def resolve_image_path(src: str, base_dir: Path) -> Path | None:
    src = html.unescape(src.strip())
    if is_remote_src(src):
        return None
    if src.startswith("data:"):
        raise WeChatError("Inline data: images are not supported. Save the image as jpg/png and reference the file.")
    if src.startswith("file://"):
        parsed = urllib.parse.urlparse(src)
        return Path(urllib.parse.unquote(parsed.path))
    candidate = Path(src)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    return candidate.resolve()


def check_inline_image(path: Path) -> None:
    require_file(path, "Inline image")
    mime = mimetypes.guess_type(path.name)[0]
    if mime not in {"image/jpeg", "image/png"}:
        raise WeChatError(f"WeChat article images must be jpg/png: {path}")
    if path.stat().st_size > INLINE_IMAGE_LIMIT:
        raise WeChatError(f"WeChat article images must be under 1 MB: {path}")


def encode_multipart(field_name: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"codex-wechat-{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8")
    footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return header + file_path.read_bytes() + footer, f"multipart/form-data; boundary={boundary}"


def request_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None
    headers: dict[str, str] = {}
    method = "GET"
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
        method = "POST"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise WeChatError(f"WeChat HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise WeChatError(f"WeChat network error: {exc}") from exc
    try:
        result = json.loads(body)
    except json.JSONDecodeError as exc:
        raise WeChatError(f"WeChat returned non-JSON response: {body[:300]}") from exc
    errcode = result.get("errcode")
    if errcode not in (None, 0):
        errmsg = result.get("errmsg", "")
        raise WeChatError(f"WeChat API error {errcode}: {errmsg}")
    return result


def request_file(url: str, field_name: str, file_path: Path, timeout: int = 60) -> dict[str, Any]:
    body, content_type = encode_multipart(field_name, file_path)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": content_type}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")
        raise WeChatError(f"WeChat HTTP {exc.code}: {text}") from exc
    except urllib.error.URLError as exc:
        raise WeChatError(f"WeChat network error: {exc}") from exc
    result = json.loads(text)
    errcode = result.get("errcode")
    if errcode not in (None, 0):
        raise WeChatError(f"WeChat API error {errcode}: {result.get('errmsg', '')}")
    return result


def get_access_token(args: argparse.Namespace) -> str:
    file_credentials = load_credentials_file()
    existing = file_credentials.get("WECHAT_ACCESS_TOKEN") or os.getenv("WECHAT_ACCESS_TOKEN")
    if existing:
        return existing
    appid = args.appid or file_credentials.get("WECHAT_APP_ID") or os.getenv("WECHAT_APP_ID")
    appsecret = args.appsecret or file_credentials.get("WECHAT_APP_SECRET") or os.getenv("WECHAT_APP_SECRET")
    if not appid or not appsecret:
        raise WeChatError(
            "Set WECHAT_ACCESS_TOKEN or WECHAT_APP_ID and WECHAT_APP_SECRET, "
            f"or save credentials in {DEFAULT_CREDENTIALS_FILE}."
        )
    query = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": appid, "secret": appsecret}
    )
    result = request_json(f"{API_BASE}/cgi-bin/token?{query}")
    token = result.get("access_token")
    if not token:
        raise WeChatError("WeChat token response did not include access_token.")
    return str(token)


def upload_article_image(token: str, path: Path) -> str:
    check_inline_image(path)
    query = urllib.parse.urlencode({"access_token": token})
    result = request_file(f"{API_BASE}/cgi-bin/media/uploadimg?{query}", "media", path)
    url = result.get("url")
    if not url:
        raise WeChatError(f"WeChat image upload did not return url for {path}")
    return str(url)


def upload_cover_material(token: str, path: Path) -> str:
    require_file(path, "Cover image")
    query = urllib.parse.urlencode({"access_token": token, "type": "image"})
    result = request_file(f"{API_BASE}/cgi-bin/material/add_material?{query}", "media", path)
    media_id = result.get("media_id")
    if not media_id:
        raise WeChatError(f"WeChat cover upload did not return media_id for {path}")
    return str(media_id)


def rewrite_inline_images(content: str, base_dir: Path, token: str | None, dry_run: bool, upload: bool) -> str:
    if not upload:
        return content
    warnings: list[str] = []

    def replace(match: re.Match[str]) -> str:
        src = match.group(3)
        path = resolve_image_path(src, base_dir)
        if path is None:
            warnings.append(f"Remote image left unchanged: {src}")
            return match.group(0)
        if dry_run:
            new_url = f"WECHAT_UPLOADED_IMAGE_URL:{path.name}"
        else:
            if token is None:
                raise WeChatError("Internal error: token is required for live image upload.")
            new_url = upload_article_image(token, path)
        return f"{match.group(1)}{match.group(2)}{html.escape(new_url, quote=True)}{match.group(2)}"

    rewritten = IMG_SRC_RE.sub(replace, content)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return rewritten


def bool_int(value: bool) -> int:
    return 1 if value else 0


def build_article_payload(args: argparse.Namespace, metadata: dict[str, Any], content: str, thumb_media_id: str) -> dict[str, Any]:
    title = args.title or metadata.get("title")
    if not title:
        raise WeChatError("Article title is required. Use --title or frontmatter/title metadata.")
    digest = args.digest or metadata.get("digest")
    if not digest:
        digest = strip_tags(content)[:120]
    article: dict[str, Any] = {
        "article_type": metadata.get("article_type", "news"),
        "title": str(title),
        "digest": str(digest),
        "content": content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": bool_int(args.open_comment or bool(metadata.get("need_open_comment"))),
        "only_fans_can_comment": bool_int(args.fans_only_comment or bool(metadata.get("only_fans_can_comment"))),
    }
    author = args.author or metadata.get("author")
    if author:
        article["author"] = str(author)
    source_url = args.source_url or metadata.get("content_source_url") or metadata.get("source_url")
    if source_url:
        article["content_source_url"] = str(source_url)
    if args.pic_crop_235_1:
        article["pic_crop_235_1"] = args.pic_crop_235_1
    if args.pic_crop_1_1:
        article["pic_crop_1_1"] = args.pic_crop_1_1
    return {"articles": [article]}


def command_draft(args: argparse.Namespace) -> None:
    article_path = Path(args.article).resolve()
    require_file(article_path, "Article")
    metadata, content = load_article(article_path)
    token = None if args.dry_run else get_access_token(args)
    content = rewrite_inline_images(
        content=content,
        base_dir=article_path.parent,
        token=token,
        dry_run=args.dry_run,
        upload=not args.no_inline_image_upload,
    )
    thumb_media_id = args.thumb_media_id or metadata.get("thumb_media_id")
    cover = args.cover or metadata.get("cover_path") or metadata.get("cover")
    if not thumb_media_id:
        if args.dry_run:
            thumb_media_id = "DRY_RUN_THUMB_MEDIA_ID"
        elif cover:
            thumb_media_id = upload_cover_material(token or "", Path(cover).expanduser().resolve())
        else:
            raise WeChatError("A cover image or --thumb-media-id is required.")
    payload = build_article_payload(args, metadata, content, str(thumb_media_id))
    if len(payload["articles"][0]["content"].encode("utf-8")) > 1024 * 1024:
        raise WeChatError("Article HTML content is over 1 MB; reduce content before uploading.")
    if args.dry_run:
        print_json({"dry_run": True, "draft_payload": payload})
        return
    query = urllib.parse.urlencode({"access_token": token})
    result = request_json(f"{API_BASE}/cgi-bin/draft/add?{query}", payload)
    print_json(result)


def command_publish(args: argparse.Namespace) -> None:
    if not args.confirm_publish:
        raise WeChatError("Refusing to publish without --confirm-publish.")
    token = get_access_token(args)
    query = urllib.parse.urlencode({"access_token": token})
    result = request_json(f"{API_BASE}/cgi-bin/freepublish/submit?{query}", {"media_id": args.media_id})
    print_json(result)


def command_status(args: argparse.Namespace) -> None:
    token = get_access_token(args)
    query = urllib.parse.urlencode({"access_token": token})
    result = request_json(f"{API_BASE}/cgi-bin/freepublish/get?{query}", {"publish_id": args.publish_id})
    print_json(result)


def add_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--appid", help="WeChat AppID. Overrides config/env credentials.")
    parser.add_argument("--appsecret", help="WeChat AppSecret. Overrides config/env credentials.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    draft = subparsers.add_parser("draft", help="Create a WeChat draft from a local article.")
    add_auth_args(draft)
    draft.add_argument("--article", required=True, help="Local HTML, Markdown, or JSON article file.")
    draft.add_argument("--cover", help="Local cover image path, used to create thumb_media_id.")
    draft.add_argument("--thumb-media-id", help="Existing WeChat thumb_media_id for the cover.")
    draft.add_argument("--title", help="Article title. Overrides source metadata.")
    draft.add_argument("--author", help="Article author. Overrides source metadata.")
    draft.add_argument("--digest", help="Article digest. Defaults to content text preview.")
    draft.add_argument("--source-url", help="Original source URL for 'Read original'.")
    draft.add_argument("--open-comment", action="store_true", help="Enable comments.")
    draft.add_argument("--fans-only-comment", action="store_true", help="Restrict comments to fans.")
    draft.add_argument("--pic-crop-235-1", help="Cover crop string x1_y1_x2_y2 for 2.35:1.")
    draft.add_argument("--pic-crop-1-1", help="Cover crop string x1_y1_x2_y2 for 1:1.")
    draft.add_argument("--no-inline-image-upload", action="store_true", help="Do not upload and rewrite local inline images.")
    draft.add_argument("--dry-run", action="store_true", help="Print payload without calling WeChat APIs.")
    draft.set_defaults(func=command_draft)

    publish = subparsers.add_parser("publish", help="Submit an existing draft for publishing.")
    add_auth_args(publish)
    publish.add_argument("--media-id", required=True, help="Draft media_id returned by draft/add.")
    publish.add_argument("--confirm-publish", action="store_true", help="Required explicit publish confirmation.")
    publish.set_defaults(func=command_publish)

    status = subparsers.add_parser("status", help="Query a publish task.")
    add_auth_args(status)
    status.add_argument("--publish-id", required=True, help="Publish task ID returned by freepublish/submit.")
    status.set_defaults(func=command_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except WeChatError as exc:
        message = str(exc)
        print(f"error: {message}", file=sys.stderr)
        hint = developer_platform_hint(message)
        if hint:
            print(f"提示：{hint}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
