#!/usr/bin/env python3
"""Manage WeChat Official Account article comments."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.weixin.qq.com"
DEVELOPER_PLATFORM_URL = "https://developers.weixin.qq.com/platform"
DEFAULT_CREDENTIALS_FILE = Path.home() / ".config" / "wechat-mp" / ".env"
COMMENT_TYPES = {"all": 0, "normal": 1, "selected": 2}


class WeChatError(RuntimeError):
    pass


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


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


def credential_value(args: argparse.Namespace, key: str, file_values: dict[str, str]) -> str | None:
    attr = {
        "WECHAT_ACCESS_TOKEN": "access_token",
        "WECHAT_APP_ID": "appid",
        "WECHAT_APP_SECRET": "appsecret",
    }[key]
    cli_value = getattr(args, attr, None)
    return cli_value or file_values.get(key) or os.environ.get(key)


def http_json(
    url: str,
    payload: dict[str, Any] | None = None,
    method: str = "POST",
    timeout: int = 30,
) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise WeChatError(f"WeChat HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise WeChatError(f"WeChat request failed: {exc.reason}") from exc
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WeChatError(f"WeChat returned non-JSON response: {raw[:500]}") from exc
    errcode = result.get("errcode")
    if errcode not in (None, 0):
        raise WeChatError(f"WeChat API error {errcode}: {result.get('errmsg', '')}")
    return result


def get_access_token(args: argparse.Namespace) -> str:
    file_values = load_credentials_file()
    access_token = credential_value(args, "WECHAT_ACCESS_TOKEN", file_values)
    if access_token:
        return access_token

    appid = credential_value(args, "WECHAT_APP_ID", file_values)
    appsecret = credential_value(args, "WECHAT_APP_SECRET", file_values)
    if not appid or not appsecret:
        raise WeChatError(
            "Set WECHAT_ACCESS_TOKEN or WECHAT_APP_ID/WECHAT_APP_SECRET in "
            f"{DEFAULT_CREDENTIALS_FILE}, environment variables, or command options."
        )
    query = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": appid, "secret": appsecret}
    )
    result = http_json(f"{API_BASE}/cgi-bin/token?{query}", payload=None, method="GET")
    token = result.get("access_token")
    if not token:
        raise WeChatError(f"WeChat token response did not include access_token: {result}")
    return str(token)


def developer_platform_hint(message: str) -> str | None:
    normalized = message.lower()
    if "set wechat_access_token" in normalized or "wechat_app_id" in normalized:
        return (
            f"请到 {DEVELOPER_PLATFORM_URL} 获取或核对公众号 AppID/AppSecret，"
            f"再写入 {DEFAULT_CREDENTIALS_FILE}。"
        )
    if "40164" in normalized or "invalid ip" in normalized or "whitelist" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 的公众号开发配置中，将当前服务器出口 IP 加入 IP 白名单。"
    if "40001" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 核对 AppID/AppSecret 或 access token 所属账号。"
    if "48001" in normalized or "88000" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 检查接口权限、账号认证状态和留言权限。"
    return None


def comment_api(token: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({"access_token": token})
    return http_json(f"{API_BASE}{path}?{query}", payload=payload, method="POST")


def base_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = {"msg_data_id": int(args.msg_data_id)}
    if args.index is not None:
        payload["index"] = int(args.index)
    return payload


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_list(args: argparse.Namespace) -> int:
    if args.count <= 0 or args.count >= 50:
        raise WeChatError("count must be between 1 and 49; WeChat rejects count >= 50.")
    request_payload = base_payload(args)
    request_payload.update(
        {
            "begin": int(args.begin),
            "count": int(args.count),
            "type": COMMENT_TYPES[args.type],
        }
    )
    if args.dry_run:
        print_json({"method": "POST", "path": "/cgi-bin/comment/list", "payload": request_payload})
        return 0

    token = get_access_token(args)
    comments: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    begin = int(args.begin)
    total: int | None = None

    while True:
        payload = dict(request_payload)
        payload["begin"] = begin
        result = comment_api(token, "/cgi-bin/comment/list", payload)
        page_comments = result.get("comment") or []
        if not isinstance(page_comments, list):
            raise WeChatError(f"Unexpected comment list response: {result}")
        pages.append({"begin": begin, "count": len(page_comments), "total": result.get("total")})
        comments.extend(page_comments)
        total = int(result.get("total", len(comments)))
        begin += len(page_comments)
        if not args.all_pages or not page_comments or begin >= total:
            break
        if len(page_comments) < args.count:
            break

    output = {
        "msg_data_id": int(args.msg_data_id),
        "index": int(args.index or 0),
        "type": args.type,
        "total": total if total is not None else len(comments),
        "fetched": len(comments),
        "pages": pages,
        "comment": redact_comments(comments, show_openid=args.show_openid),
    }
    if args.output:
        write_json(Path(args.output), output)
    print_json(output)
    return 0


def command_state_action(args: argparse.Namespace, path: str, extra: dict[str, Any] | None = None) -> int:
    payload = base_payload(args)
    if getattr(args, "comment_id", None) is not None:
        payload["user_comment_id"] = int(args.comment_id)
    if extra:
        payload.update(extra)
    preview = {"method": "POST", "path": path, "payload": payload}
    if args.dry_run or not args.confirm:
        preview["dry_run"] = True
        preview["note"] = "Add --confirm without --dry-run to execute this online change."
        print_json(preview)
        return 0
    token = get_access_token(args)
    result = comment_api(token, path, payload)
    print_json({"executed": True, "path": path, "payload": payload, "response": result})
    return 0


def read_content_arg(args: argparse.Namespace) -> str:
    if args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8").strip()
    else:
        content = (args.content or "").strip()
    if not content:
        raise WeChatError("Reply content must not be empty.")
    return content


def command_reply(args: argparse.Namespace) -> int:
    return command_state_action(args, "/cgi-bin/comment/reply/add", {"content": read_content_arg(args)})


def redact_comments(comments: list[dict[str, Any]], show_openid: bool = False) -> list[dict[str, Any]]:
    if show_openid:
        return comments
    redacted: list[dict[str, Any]] = []
    for comment in comments:
        item = dict(comment)
        if "openid" in item:
            value = str(item.get("openid") or "")
            item["openid"] = f"{value[:6]}...{value[-4:]}" if len(value) > 12 else "[redacted]"
        redacted.append(item)
    return redacted


def flatten_comments(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        raw = value.get("comment") or value.get("comments")
        if isinstance(raw, list):
            return [x for x in raw if isinstance(x, dict)]
        if isinstance(value.get("pages"), list):
            comments: list[dict[str, Any]] = []
            for page in value["pages"]:
                if isinstance(page, dict) and isinstance(page.get("comment"), list):
                    comments.extend(x for x in page["comment"] if isinstance(x, dict))
            return comments
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict)]
    raise WeChatError("Input JSON must contain a comment array.")


def classify_comment(content: str) -> str:
    text = content.strip()
    if re.search(r"(吗|呢|怎么|如何|为什么|请问|\?)", text):
        return "问题"
    if re.search(r"(谢谢|有用|赞|受益|收藏|清楚|喜欢)", text):
        return "正向反馈"
    if re.search(r"(错误|不对|失败|问题|投诉|广告|退款|无法|不能)", text):
        return "需处理"
    if len(text) >= 80:
        return "长观点"
    return "一般反馈"


def render_report(comments: list[dict[str, Any]]) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    selected = [c for c in comments if int(c.get("comment_type") or 0) == 1]
    replied = [c for c in comments if isinstance(c.get("reply"), dict) and c["reply"].get("content")]
    buckets: dict[str, list[dict[str, Any]]] = {}
    for comment in comments:
        bucket = classify_comment(str(comment.get("content") or ""))
        buckets.setdefault(bucket, []).append(comment)

    lines = [
        "# 公众号留言分析",
        "",
        f"- 生成时间：{now}",
        f"- 留言总数：{len(comments)}",
        f"- 已精选：{len(selected)}",
        f"- 已回复：{len(replied)}",
        "",
        "## 分类概览",
        "",
    ]
    for bucket, items in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.append(f"- {bucket}：{len(items)} 条")

    lines.extend(["", "## 候选精选", ""])
    candidates = sorted(
        comments,
        key=lambda c: (int(c.get("comment_type") or 0), len(str(c.get("content") or ""))),
        reverse=True,
    )[:10]
    if not candidates:
        lines.append("暂无留言。")
    for comment in candidates:
        content = str(comment.get("content") or "").replace("\n", " ")
        lines.append(f"- `{comment.get('user_comment_id')}`：{content[:160]}")

    lines.extend(["", "## 建议回复的问题", ""])
    questions = buckets.get("问题", [])[:10]
    if not questions:
        lines.append("暂无明显问题型留言。")
    for comment in questions:
        content = str(comment.get("content") or "").replace("\n", " ")
        lines.append(f"- `{comment.get('user_comment_id')}`：{content[:160]}")
        lines.append("  建议回复：谢谢提问，这里可以补充说明为：...")

    lines.extend(["", "## 需谨慎处理", ""])
    risky = buckets.get("需处理", [])[:10]
    if not risky:
        lines.append("暂无明显需谨慎处理留言。")
    for comment in risky:
        content = str(comment.get("content") or "").replace("\n", " ")
        lines.append(f"- `{comment.get('user_comment_id')}`：{content[:160]}")
    lines.append("")
    return "\n".join(lines)


def command_analyze(args: argparse.Namespace) -> int:
    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    comments = redact_comments(flatten_comments(raw), show_openid=args.show_openid)
    report = render_report(comments)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    print(report)
    return 0


def add_common_article_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--msg-data-id", required=True, help="Article msg_data_id returned by WeChat.")
    parser.add_argument("--index", type=int, default=0, help="Article index in a multi-article message, starting at 0.")
    parser.add_argument("--dry-run", action="store_true", help="Print the request without calling WeChat.")
    parser.add_argument("--confirm", action="store_true", help="Execute an online state-changing action.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--access-token", help="Use an existing WECHAT_ACCESS_TOKEN.")
    parser.add_argument("--appid", help="WeChat AppID used to fetch access_token.")
    parser.add_argument("--appsecret", help="WeChat AppSecret used to fetch access_token.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List article comments.")
    add_common_article_args(list_parser)
    list_parser.add_argument("--begin", type=int, default=0, help="Comment offset.")
    list_parser.add_argument("--count", type=int, default=49, help="Page size. Must be 1-49.")
    list_parser.add_argument("--type", choices=sorted(COMMENT_TYPES), default="all")
    list_parser.add_argument("--all-pages", action="store_true", help="Fetch all pages until total is reached.")
    list_parser.add_argument("--show-openid", action="store_true", help="Do not redact openid in output.")
    list_parser.add_argument("--output", help="Write JSON result to this file.")
    list_parser.set_defaults(func=command_list)

    actions = {
        "open": ("/cgi-bin/comment/open", "Open article comments."),
        "close": ("/cgi-bin/comment/close", "Close article comments."),
        "elect": ("/cgi-bin/comment/markelect", "Mark a comment as selected."),
        "unelect": ("/cgi-bin/comment/unmarkelect", "Unmark a selected comment."),
        "delete": ("/cgi-bin/comment/delete", "Delete a comment."),
        "delete-reply": ("/cgi-bin/comment/reply/delete", "Delete a comment reply."),
    }
    for name, (path, help_text) in actions.items():
        action_parser = subparsers.add_parser(name, help=help_text)
        add_common_article_args(action_parser)
        if name not in {"open", "close"}:
            action_parser.add_argument("--comment-id", required=True, help="user_comment_id.")
        action_parser.set_defaults(func=lambda a, p=path: command_state_action(a, p))

    reply_parser = subparsers.add_parser("reply", help="Reply to a comment.")
    add_common_article_args(reply_parser)
    reply_parser.add_argument("--comment-id", required=True, help="user_comment_id.")
    reply_group = reply_parser.add_mutually_exclusive_group(required=True)
    reply_group.add_argument("--content", help="Reply text.")
    reply_group.add_argument("--content-file", help="Read reply text from a UTF-8 file.")
    reply_parser.set_defaults(func=command_reply)

    analyze_parser = subparsers.add_parser("analyze", help="Create a local Markdown analysis from exported comments.")
    analyze_parser.add_argument("--input", required=True, help="Input JSON produced by the list command.")
    analyze_parser.add_argument("--output", help="Write Markdown report to this file.")
    analyze_parser.add_argument("--show-openid", action="store_true", help="Do not redact openid in analysis output.")
    analyze_parser.set_defaults(func=command_analyze)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except WeChatError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        hint = developer_platform_hint(str(exc))
        if hint:
            print(hint, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
