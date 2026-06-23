---
name: wechat-article-comments
description: 管理微信公众号已发布文章的留言评论，包括拉取留言、整理精选建议、生成回复草稿、打开或关闭评论、精选或取消精选、删除留言、回复留言和删除回复。Use when Codex needs to moderate WeChat Official Account article comments, analyze reader feedback, prepare reply recommendations, or call official comment APIs for published articles with msg_data_id/index/user_comment_id.
---

# 微信公众号留言管理

## 定位

围绕公众号已群发或已发表文章的留言区做运营辅助。默认先拉取和分析留言，再给出精选、回复和风险处理建议；任何会改变线上状态的动作都必须经过 dry-run 和用户确认。

## 核心输入

- `msg_data_id`：群发或发表内容对应的消息数据 ID。
- `index`：多图文中的文章序号，从 0 开始；未提供时按 0 处理。
- `user_comment_id`：指定留言 ID，精选、回复、删除等动作必需。
- 评论范围：全部、普通留言或精选留言。

如果用户只提供文章标题或本地文章文件，先说明仍需要 `msg_data_id`；不要凭标题猜测线上文章 ID。

## 工作流

1. 明确目标：拉取留言、做运营分析、生成回复草稿，还是执行精选/回复/删除等线上动作。
2. 如涉及官方接口，读取 `references/api.md`，确认参数、权限和风险边界。
3. 使用 `scripts/wechat_article_comments.py list --dry-run` 先检查请求载荷；真实拉取时再去掉 `--dry-run`。
4. 将留言导出到工作区 `outputs/wechat-comments/`，优先保留 JSON 原始数据，再生成 Markdown 分析稿。
5. 分析留言时按这些维度整理：
   - 值得精选：观点清楚、补充案例、代表多数读者疑问、表达克制。
   - 适合回复：真实问题、误解澄清、可转化为后续选题的问题。
   - 谨慎处理：攻击、人身信息、广告、诱导、明显违规或可能引发争议的内容。
6. 生成回复草稿时保持公众号口吻：简短、具体、尊重读者，不争辩，不暴露内部信息。
7. 执行线上变更前，先运行对应命令的 `--dry-run` 并向用户复述将影响的文章、留言 ID 和动作。
8. 只有用户明确确认后，才添加 `--confirm` 执行精选、取消精选、删除、回复、删除回复、打开或关闭评论。

## 命令

列出留言：

```bash
python wechat-article-comments/scripts/wechat_article_comments.py list \
  --msg-data-id MSG_DATA_ID \
  --index 0 \
  --type all \
  --all-pages \
  --output outputs/wechat-comments/comments.json
```

生成本地分析稿：

```bash
python wechat-article-comments/scripts/wechat_article_comments.py analyze \
  --input outputs/wechat-comments/comments.json \
  --output outputs/wechat-comments/comments-report.md
```

回复留言前预览：

```bash
python wechat-article-comments/scripts/wechat_article_comments.py reply \
  --msg-data-id MSG_DATA_ID \
  --index 0 \
  --comment-id USER_COMMENT_ID \
  --content "谢谢补充，这个角度很有价值。" \
  --dry-run
```

确认执行：

```bash
python wechat-article-comments/scripts/wechat_article_comments.py reply \
  --msg-data-id MSG_DATA_ID \
  --index 0 \
  --comment-id USER_COMMENT_ID \
  --content "谢谢补充，这个角度很有价值。" \
  --confirm
```

## 凭据

脚本读取顺序与发布节点保持一致：

- `~/.config/wechat-mp/.env` 中的 `WECHAT_ACCESS_TOKEN`、`WECHAT_APP_ID`、`WECHAT_APP_SECRET`。
- 当前环境变量中的同名字段。
- 命令行参数 `--access-token`、`--appid`、`--appsecret`。

不要在回复、日志或仓库文件中回显 AppSecret。遇到 `40001`、`40164`、`48001`、`88000` 等配置或权限问题时，提示用户到 `https://developers.weixin.qq.com/platform` 核对 AppID/AppSecret、IP 白名单、接口权限、账号认证和留言权限。

## 安全边界

- 默认只读取和分析留言。
- 删除留言、回复留言、删除回复、精选/取消精选、打开/关闭评论都属于线上状态变更，必须要求用户当轮确认。
- 不要批量删除或批量回复，除非用户明确给出留言 ID 清单并确认每一类动作。
- 输出分析报告时默认隐藏 `openid`；只有用户明确需要排查身份关联时才保留。
- 不要自动回复涉及隐私、投诉、法律、医疗、财务或安全风险的问题；只给草稿和人工处理建议。

## 输出

最终回复保持短而清楚：

- 已拉取多少条留言、是否还有分页。
- 生成的 JSON 和 Markdown 文件路径。
- 推荐精选/回复/删除的候选数量。
- 如执行了线上动作，给出动作、留言 ID 和微信接口返回摘要。
