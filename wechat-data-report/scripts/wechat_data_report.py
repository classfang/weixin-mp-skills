#!/usr/bin/env python3
"""Fetch WeChat Official Account analytics data and render reports."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.weixin.qq.com"
DEVELOPER_PLATFORM_URL = "https://developers.weixin.qq.com/platform"
DEFAULT_CREDENTIALS_FILE = Path.home() / ".config" / "wechat-mp" / ".env"
DEFAULT_OUTPUT_DIR = Path("outputs") / "wechat-data-report"

DATASETS: dict[str, dict[str, Any]] = {
    "user-summary": {"path": "/datacube/getusersummary", "label": "用户增减", "max_days": 7, "group": "user"},
    "user-cumulate": {"path": "/datacube/getusercumulate", "label": "累计用户", "max_days": 7, "group": "user"},
    "article-summary-legacy": {
        "path": "/datacube/getarticlesummary",
        "label": "图文群发每日数据（旧）",
        "max_days": 1,
        "group": "article",
        "legacy": True,
    },
    "article-total-legacy": {
        "path": "/datacube/getarticletotal",
        "label": "图文群发总数据（旧）",
        "max_days": 1,
        "group": "article",
        "legacy": True,
    },
    "article-read": {"path": "/datacube/getuserread", "label": "图文阅读概况", "max_days": 1, "group": "article"},
    "article-read-hour": {
        "path": "/datacube/getuserreadhour",
        "label": "图文阅读分时",
        "max_days": 1,
        "group": "article",
    },
    "article-share": {"path": "/datacube/getusershare", "label": "图文分享概况", "max_days": 1, "group": "article"},
    "article-share-hour": {
        "path": "/datacube/getusersharehour",
        "label": "图文分享分时",
        "max_days": 1,
        "group": "article",
    },
    "article-daily-read": {
        "path": "/datacube/getarticleread",
        "label": "发表内容每日阅读",
        "max_days": 1,
        "group": "article",
    },
    "article-daily-share": {
        "path": "/datacube/getarticleshare",
        "label": "发表内容每日分享",
        "max_days": 1,
        "group": "article",
    },
    "biz-summary": {"path": "/datacube/getbizsummary", "label": "发表内容概况", "max_days": 1, "group": "article"},
    "article-total-detail": {
        "path": "/datacube/getarticletotaldetail",
        "label": "发表内容详细",
        "max_days": 1,
        "group": "article",
    },
    "message-summary": {"path": "/datacube/getupstreammsg", "label": "消息发送概况", "max_days": 7, "group": "message"},
    "message-hour": {"path": "/datacube/getupstreammsghour", "label": "消息发送分时", "max_days": 1, "group": "message"},
    "message-week": {"path": "/datacube/getupstreammsgweek", "label": "消息发送周", "max_days": 30, "group": "message"},
    "message-month": {"path": "/datacube/getupstreammsgmonth", "label": "消息发送月", "max_days": 30, "group": "message"},
    "message-dist": {"path": "/datacube/getupstreammsgdist", "label": "消息发送分布", "max_days": 7, "group": "message"},
    "message-dist-week": {
        "path": "/datacube/getupstreammsgdistweek",
        "label": "消息发送分布周",
        "max_days": 30,
        "group": "message",
    },
    "message-dist-month": {
        "path": "/datacube/getupstreammsgdistmonth",
        "label": "消息发送分布月",
        "max_days": 30,
        "group": "message",
    },
    "interface-summary": {
        "path": "/datacube/getinterfacesummary",
        "label": "被动回复概要",
        "max_days": 30,
        "group": "interface",
    },
    "interface-hour": {
        "path": "/datacube/getinterfacesummaryhour",
        "label": "被动回复分时",
        "max_days": 1,
        "group": "interface",
    },
}

DEFAULT_DATASETS = [
    "user-summary",
    "user-cumulate",
    "article-daily-read",
    "article-daily-share",
    "biz-summary",
    "article-total-detail",
]

USER_SOURCE_LABELS = {
    0: "其他合计",
    1: "公众号搜索",
    17: "名片分享",
    30: "扫描二维码",
    57: "文章内账号名称",
    100: "微信广告",
    149: "小程序关注",
    161: "他人转载",
    200: "视频号",
    201: "直播",
}


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
    if "48001" in normalized:
        return f"请到 {DEVELOPER_PLATFORM_URL} 检查数据统计接口权限和账号认证状态。"
    if "61500" in normalized or "61501" in normalized:
        return "请缩短查询日期范围，或按天分片查询图文/发表内容类接口。"
    if "61503" in normalized:
        return "指定日期数据尚未生成。官方建议每天上午 8 点后查询前一天数据。"
    return None


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise WeChatError(f"Invalid date '{value}', expected YYYY-MM-DD.") from exc


def date_chunks(begin: dt.date, end: dt.date, max_days: int) -> list[tuple[dt.date, dt.date]]:
    if begin > end:
        raise WeChatError("begin date must be earlier than or equal to end date.")
    chunks: list[tuple[dt.date, dt.date]] = []
    cursor = begin
    step = dt.timedelta(days=max_days - 1)
    while cursor <= end:
        chunk_end = min(cursor + step, end)
        chunks.append((cursor, chunk_end))
        cursor = chunk_end + dt.timedelta(days=1)
    return chunks


def parse_dataset_names(value: str | None) -> list[str]:
    names = DEFAULT_DATASETS if not value else [item.strip() for item in value.split(",") if item.strip()]
    unknown = [name for name in names if name not in DATASETS]
    if unknown:
        raise WeChatError(f"Unknown dataset(s): {', '.join(unknown)}")
    return names


def datacube_api(token: str, path: str, begin: dt.date, end: dt.date) -> dict[str, Any]:
    query = urllib.parse.urlencode({"access_token": token})
    payload = {"begin_date": begin.isoformat(), "end_date": end.isoformat()}
    return http_json(f"{API_BASE}{path}?{query}", payload=payload, method="POST")


def planned_requests(
    dataset_names: list[str],
    begin: dt.date,
    end: dt.date,
    chunk_days_override: int | None = None,
) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    for name in dataset_names:
        info = DATASETS[name]
        max_days = int(chunk_days_override or info["max_days"])
        for chunk_begin, chunk_end in date_chunks(begin, end, max_days):
            requests.append(
                {
                    "dataset": name,
                    "label": info["label"],
                    "path": info["path"],
                    "begin_date": chunk_begin.isoformat(),
                    "end_date": chunk_end.isoformat(),
                    "payload": {"begin_date": chunk_begin.isoformat(), "end_date": chunk_end.isoformat()},
                    "legacy": bool(info.get("legacy")),
                }
            )
    return requests


def safe_yesterday() -> dt.date:
    return dt.date.today() - dt.timedelta(days=1)


def command_datasets(args: argparse.Namespace) -> int:
    rows = []
    for name, info in DATASETS.items():
        rows.append(
            {
                "name": name,
                "label": info["label"],
                "path": info["path"],
                "max_days": info["max_days"],
                "group": info["group"],
                "legacy": bool(info.get("legacy")),
            }
        )
    print_json(rows)
    return 0


def command_fetch(args: argparse.Namespace) -> int:
    begin = parse_date(args.begin)
    end = parse_date(args.end)
    if not args.allow_today and end > safe_yesterday():
        raise WeChatError(
            f"end date {end.isoformat()} is newer than yesterday. "
            "Use --allow-today only when you accept incomplete data."
        )
    if begin < dt.date(2014, 12, 1):
        raise WeChatError("WeChat analytics data before 2014-12-01 is not reliable or unavailable.")

    dataset_names = parse_dataset_names(args.datasets)
    requests = planned_requests(dataset_names, begin, end, args.chunk_days)
    if args.dry_run:
        print_json({"begin_date": begin.isoformat(), "end_date": end.isoformat(), "requests": requests})
        return 0

    token = get_access_token(args)
    results: list[dict[str, Any]] = []
    for request in requests:
        try:
            response = datacube_api(
                token,
                str(request["path"]),
                parse_date(str(request["begin_date"])),
                parse_date(str(request["end_date"])),
            )
            results.append({**request, "response": response})
        except WeChatError as exc:
            if not args.continue_on_error:
                raise
            results.append({**request, "error": str(exc)})

    output = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "begin_date": begin.isoformat(),
        "end_date": end.isoformat(),
        "datasets": dataset_names,
        "results": results,
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{begin.isoformat()}_{end.isoformat()}"
    json_path = output_dir / f"wechat-data-{stem}.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_path: Path | None = None
    if not args.no_report:
        report_path = output_dir / f"wechat-data-report-{stem}.md"
        report_path.write_text(render_report(output), encoding="utf-8")

    print_json(
        {
            "raw_json": str(json_path),
            "report": str(report_path) if report_path else None,
            "requests": len(requests),
            "errors": sum(1 for item in results if "error" in item),
        }
    )
    return 0


def numeric(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except ValueError:
            return 0
    return 0


def response_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    response = result.get("response")
    if not isinstance(response, dict):
        return []
    rows = response.get("list")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


def collect_rows(data: dict[str, Any], group: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for result in data.get("results", []):
        if not isinstance(result, dict):
            continue
        dataset = str(result.get("dataset") or "")
        if group and DATASETS.get(dataset, {}).get("group") != group:
            continue
        for row in response_rows(result):
            rows.append((dataset, row))
    return rows


def render_user_section(data: dict[str, Any]) -> list[str]:
    rows = collect_rows(data, "user")
    summary_rows = [row for dataset, row in rows if dataset == "user-summary"]
    cumulate_rows = [row for dataset, row in rows if dataset == "user-cumulate"]
    new_user = sum(numeric(row.get("new_user")) for row in summary_rows)
    cancel_user = sum(numeric(row.get("cancel_user")) for row in summary_rows)
    latest_cumulate = None
    for row in sorted(cumulate_rows, key=lambda item: str(item.get("ref_date", ""))):
        if row.get("cumulate_user") is not None:
            latest_cumulate = numeric(row.get("cumulate_user"))

    lines = ["## 用户", ""]
    lines.append(f"- 新增关注：{new_user}")
    lines.append(f"- 取消关注：{cancel_user}")
    lines.append(f"- 净增关注：{new_user - cancel_user}")
    if latest_cumulate is not None:
        lines.append(f"- 最新累计用户：{latest_cumulate}")

    by_source: dict[int, dict[str, int]] = {}
    for row in summary_rows:
        source = numeric(row.get("user_source"))
        bucket = by_source.setdefault(source, {"new": 0, "cancel": 0})
        bucket["new"] += numeric(row.get("new_user"))
        bucket["cancel"] += numeric(row.get("cancel_user"))
    if by_source:
        lines.extend(["", "### 来源渠道", ""])
        for source, values in sorted(by_source.items(), key=lambda item: -item[1]["new"])[:10]:
            label = USER_SOURCE_LABELS.get(source, f"来源 {source}")
            lines.append(f"- {label}：新增 {values['new']}，取关 {values['cancel']}，净增 {values['new'] - values['cancel']}")
    return lines


def article_key(row: dict[str, Any]) -> str:
    return str(row.get("title") or row.get("article_title") or row.get("msgid") or row.get("ref_date") or "未命名内容")


def article_metric(row: dict[str, Any], *names: str) -> int:
    return sum(numeric(row.get(name)) for name in names)


def render_article_section(data: dict[str, Any]) -> list[str]:
    rows = [row for _, row in collect_rows(data, "article")]
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = article_key(row)
        item = grouped.setdefault(
            key,
            {
                "title": key,
                "read_user": 0,
                "read_count": 0,
                "share_user": 0,
                "share_count": 0,
                "fav_user": 0,
                "fav_count": 0,
            },
        )
        item["read_user"] += article_metric(row, "int_page_read_user", "read_user", "user_read_user")
        item["read_count"] += article_metric(row, "int_page_read_count", "read_count", "user_read_count")
        item["share_user"] += article_metric(row, "share_user", "user_share_user")
        item["share_count"] += article_metric(row, "share_count", "user_share_count")
        item["fav_user"] += article_metric(row, "add_to_fav_user", "fav_user")
        item["fav_count"] += article_metric(row, "add_to_fav_count", "fav_count")

    totals = {
        "read_user": sum(item["read_user"] for item in grouped.values()),
        "read_count": sum(item["read_count"] for item in grouped.values()),
        "share_user": sum(item["share_user"] for item in grouped.values()),
        "share_count": sum(item["share_count"] for item in grouped.values()),
        "fav_user": sum(item["fav_user"] for item in grouped.values()),
        "fav_count": sum(item["fav_count"] for item in grouped.values()),
    }

    lines = ["## 内容", ""]
    lines.append(f"- 内容记录数：{len(rows)}")
    lines.append(f"- 阅读人数合计：{totals['read_user']}")
    lines.append(f"- 阅读次数合计：{totals['read_count']}")
    lines.append(f"- 分享人数合计：{totals['share_user']}")
    lines.append(f"- 分享次数合计：{totals['share_count']}")
    lines.append(f"- 收藏人数合计：{totals['fav_user']}")
    lines.append(f"- 收藏次数合计：{totals['fav_count']}")

    top_articles = sorted(grouped.values(), key=lambda item: (item["read_count"], item["read_user"]), reverse=True)[:10]
    if top_articles:
        lines.extend(["", "### 阅读 Top 内容", ""])
        for item in top_articles:
            lines.append(
                "- {title}：阅读 {read_count}/{read_user}，分享 {share_count}，收藏 {fav_count}".format(**item)
            )
    return lines


def render_message_section(data: dict[str, Any]) -> list[str]:
    rows = [row for _, row in collect_rows(data, "message")]
    msg_user = sum(article_metric(row, "msg_user", "msg_user_sum") for row in rows)
    msg_count = sum(article_metric(row, "msg_count", "msg_count_sum") for row in rows)
    lines = ["## 消息", "", f"- 消息人数合计：{msg_user}", f"- 消息次数合计：{msg_count}"]
    if not rows:
        lines.append("- 未拉取消息数据集。")
    return lines


def render_interface_section(data: dict[str, Any]) -> list[str]:
    rows = [row for _, row in collect_rows(data, "interface")]
    callback_count = sum(article_metric(row, "callback_count", "fail_count", "total_time_cost") for row in rows)
    lines = ["## 接口", "", f"- 接口记录数：{len(rows)}"]
    if rows:
        lines.append(f"- 可汇总数值合计：{callback_count}")
    else:
        lines.append("- 未拉取接口数据集。")
    return lines


def render_report(data: dict[str, Any]) -> str:
    generated_at = data.get("generated_at") or dt.datetime.now().isoformat(timespec="seconds")
    lines = [
        "# 微信公众号数据报表",
        "",
        f"- 生成时间：{generated_at}",
        f"- 日期范围：{data.get('begin_date')} 至 {data.get('end_date')}",
        f"- 数据集：{', '.join(data.get('datasets', []))}",
        "",
        "> 注：官方建议每日 8 点后查询前一天数据；低阅读量内容可能不返回图文统计。",
        "",
    ]
    errors = [item for item in data.get("results", []) if isinstance(item, dict) and item.get("error")]
    if errors:
        lines.extend(["## 拉取错误", ""])
        for item in errors:
            lines.append(f"- {item.get('dataset')} {item.get('begin_date')} 至 {item.get('end_date')}：{item.get('error')}")
        lines.append("")

    sections = [
        render_user_section(data),
        render_article_section(data),
        render_message_section(data),
        render_interface_section(data),
    ]
    for section in sections:
        lines.extend(section)
        lines.append("")

    lines.extend(
        [
            "## 复盘提示",
            "",
            "- 结合文章标题、封面、发布时间和推送位置解释阅读差异。",
            "- 关注分享和收藏高于阅读的内容，它们往往更适合做二次分发或系列化。",
            "- 取关峰值需要结合推送频率、选题争议度和标题预期差排查。",
            "- 空数据先检查权限、日期和统计延迟，不直接判定为表现为 0。",
            "",
        ]
    )
    return "\n".join(lines)


def command_report(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = render_report(data)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    print(report)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--access-token", help="Use an existing WECHAT_ACCESS_TOKEN.")
    parser.add_argument("--appid", help="WeChat AppID used to fetch access_token.")
    parser.add_argument("--appsecret", help="WeChat AppSecret used to fetch access_token.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    datasets_parser = subparsers.add_parser("datasets", help="List built-in datasets.")
    datasets_parser.set_defaults(func=command_datasets)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch analytics data and write JSON/Markdown outputs.")
    fetch_parser.add_argument("--begin", required=True, help="Start date, YYYY-MM-DD.")
    fetch_parser.add_argument("--end", required=True, help="End date, YYYY-MM-DD. Defaults should be yesterday or earlier.")
    fetch_parser.add_argument(
        "--datasets",
        help="Comma-separated dataset names. Defaults to user/content core datasets.",
    )
    fetch_parser.add_argument("--chunk-days", type=int, help="Override per-request date chunk size.")
    fetch_parser.add_argument("--allow-today", action="store_true", help="Allow end date newer than yesterday.")
    fetch_parser.add_argument("--continue-on-error", action="store_true", help="Keep fetching remaining datasets after errors.")
    fetch_parser.add_argument("--dry-run", action="store_true", help="Print planned requests without calling WeChat.")
    fetch_parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for report outputs.")
    fetch_parser.add_argument("--no-report", action="store_true", help="Only write raw JSON.")
    fetch_parser.set_defaults(func=command_fetch)

    report_parser = subparsers.add_parser("report", help="Render a Markdown report from a raw JSON export.")
    report_parser.add_argument("--input", required=True, help="Raw JSON produced by fetch.")
    report_parser.add_argument("--output", help="Write Markdown report to this file.")
    report_parser.set_defaults(func=command_report)
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
