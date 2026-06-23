---
name: wechat-data-report
description: 拉取微信公众号/服务号官方数据统计接口并生成运营报表，包括用户增减、累计用户、图文阅读、分享、收藏、发表内容概况、消息发送和接口调用数据。Use when Codex needs to fetch WeChat Official Account datacube metrics, build daily/weekly/monthly reports, analyze article performance, compare content results, or create Markdown/JSON data exports from official WeChat analytics APIs.
---

# 微信公众号数据报表

## 定位

从微信公众号官方数据统计接口拉取运营数据，并生成可复盘的本地 JSON 和 Markdown 报表。默认适合日常日报、周报、月报、文章表现复盘和选题反馈分析。

## 适用场景

- “拉取公众号近 7 天数据，做一份运营周报。”
- “分析最近文章阅读、分享、收藏表现。”
- “导出用户新增、取关、累计用户数据。”
- “比较不同标题或选题的阅读表现。”
- “把公众号数据整理成 Markdown 报告。”

如果用户要分析文章评论，使用 `$wechat-article-comments`；如果用户要创建草稿或发布文章，使用 `$wechat-article-publish`。

## 工作流

1. 明确账号类型、日期范围和报表目标。
2. 若要调用官方接口，读取 `references/api.md`，确认数据集、日期限制和权限要求。
3. 优先查询昨天及更早数据。微信官方建议每天上午 8 点后查询前一天数据；当天数据通常不完整。
4. 先运行 `scripts/wechat_data_report.py fetch --dry-run`，检查将请求的数据集和日期分片。
5. 去掉 `--dry-run` 拉取数据，默认输出到 `outputs/wechat-data-report/`。
6. 使用脚本生成 Markdown 报表；再由 Codex 补充业务解读、异常原因假设和下一步内容建议。
7. 最终回复只汇报文件路径、关键指标和下一步建议，不粘贴完整原始 JSON。

## 命令

查看可用数据集：

```bash
python wechat-data-report/scripts/wechat_data_report.py datasets
```

预览近 7 天请求：

```bash
python wechat-data-report/scripts/wechat_data_report.py fetch \
  --begin 2026-06-16 \
  --end 2026-06-22 \
  --dry-run
```

拉取默认报表数据并生成 Markdown：

```bash
python wechat-data-report/scripts/wechat_data_report.py fetch \
  --begin 2026-06-16 \
  --end 2026-06-22 \
  --output-dir outputs/wechat-data-report
```

从已有原始 JSON 重新生成报告：

```bash
python wechat-data-report/scripts/wechat_data_report.py report \
  --input outputs/wechat-data-report/wechat-data-2026-06-16_2026-06-22.json \
  --output outputs/wechat-data-report/wechat-data-report-2026-06-16_2026-06-22.md
```

指定数据集：

```bash
python wechat-data-report/scripts/wechat_data_report.py fetch \
  --begin 2026-06-16 \
  --end 2026-06-22 \
  --datasets user-summary,user-cumulate,article-daily-read,article-daily-share,biz-summary
```

## 凭据

脚本读取顺序：

- `~/.config/wechat-mp/.env` 中的 `WECHAT_ACCESS_TOKEN`、`WECHAT_APP_ID`、`WECHAT_APP_SECRET`。
- 当前环境变量中的同名字段。
- 命令行参数 `--access-token`、`--appid`、`--appsecret`。

不要在回复、日志或仓库文件中回显 AppSecret。遇到 `40001`、`40164`、`48001`、`61500`、`61501`、`61503` 等错误时，提示用户到 `https://developers.weixin.qq.com/platform` 核对 AppID/AppSecret、IP 白名单、接口权限、账号认证状态和数据是否已生成。

## 报表解读

生成运营复盘时优先关注：

- 用户：新增、取关、净增、累计用户，以及主要来源渠道。
- 内容：阅读人数、阅读次数、分享人数、分享次数、收藏人数、收藏次数。
- 传播：分享率、收藏率、阅读深度；小样本数据不要过度解释。
- 时间：分时阅读/分享峰值，用于判断推送时间和二次分发窗口。
- 消息：用户上行消息量和关键词变化，提示后续选题或客服需求。
- 接口：被动回复和接口调用异常，用于排查技术问题。

## 数据边界

- 官方数据接口通常只面向认证公众号/服务号。
- 官方文档提示数据接口库从 2014-12-01 后开始可查；更早数据不可信。
- 图文/发表内容数据可能因阅读量太低无法统计；不要把空结果等同于 0 表现。
- 建议本地缓存已拉取数据，减少重复调用和频率消耗。
- 当用户要求“今天数据”时，明确说明当前日期和官方统计延迟，建议改查昨天或更早。

## 输出

默认产出：

- 原始 JSON：`outputs/wechat-data-report/wechat-data-BEGIN_END.json`
- Markdown 报表：`outputs/wechat-data-report/wechat-data-report-BEGIN_END.md`

最终回复给出：

- 查询日期范围和数据集。
- 原始数据与报表文件路径。
- 3-5 条关键发现。
- 需要人工判断或补充上下文的异常点。
