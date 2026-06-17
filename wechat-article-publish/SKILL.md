---
name: wechat-article-publish
description: 通过微信公众号官方服务端 API 将本地文章发布素材推送到公众号后台，默认创建草稿而不是直接发布。Use when Codex needs to upload WeChat Official Account HTML, Markdown, or JSON articles, upload and rewrite local in-article images, create draft articles, publish only after explicit confirmation, or query publication status.
---

# 微信公众号文章发布

使用微信公众号官方服务端 API，将文章创作和文章配图节点产出的本地素材移动到公众号后台。默认创建草稿；只有当用户在当前轮次明确要求发布时，才提交草稿发布。

## 定位

发布节点只处理素材上传、草稿创建、发布确认和状态查询。不要在这个节点重写文章或生成图片；如果缺少正文或封面图，先提示用户使用 `$wechat-article-write` 或 `$wechat-article-image` 补齐。

## 工作流

1. 读取本地文章并识别格式：
   - HTML/HTM：如果存在 body，使用 body 内容。
   - Markdown：如果存在 frontmatter，先解析元数据，再转换为 HTML。
   - JSON：接受单篇文章对象，或包含 `articles` 数组的对象。
2. 发布脚本会在上传文内图片前自动清理正文：移除正文开头的封面图副本和主标题 `<h1>`，因为微信公众号的封面与标题由 `thumb_media_id` 和 `title` 字段独立展示，不应重复放在 `content` 中。
3. 发布脚本会在上传前自动把 `<pre>` 代码块归一化为微信公众号更稳定的 `<p>` + `<br>` + `&nbsp;` 结构，避免草稿中丢失换行和缩进。
4. 在任何真实 API 调用前确认必需字段：`title`、HTML `content`，以及封面图片路径或 `thumb_media_id`。
5. 先运行 `scripts/wechat_mp_publish.py draft --dry-run` 检查载荷并捕获缺失字段；确认 dry-run payload 的 `content` 中没有正文封面图副本和主标题；含代码块的文章还要确认正文中没有 `<pre`，并且保留了 `<br>` 和 `&nbsp;`。
6. 使用同一命令去掉 `--dry-run` 创建草稿。
7. 只有在用户明确确认后才发布，命令为 `scripts/wechat_mp_publish.py publish --media-id MEDIA_ID --confirm-publish`。
8. 使用 `scripts/wechat_mp_publish.py status --publish-id PUBLISH_ID` 查询发布状态。

## 凭据

从本地配置文件、环境变量或命令参数读取凭据：

- `~/.config/wechat-mp/.env`：推荐的持久化本地配置，用于保存 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`；脚本会按当前用户的 home 目录读取。
- `WECHAT_ACCESS_TOKEN`：使用现有有效 token 并跳过 AppSecret；脚本会先读取配置文件，再读取环境变量。
- `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`：用于向微信获取 access token；未提供命令参数时，脚本会先读取配置文件，再读取环境变量。
- `--appid` 和 `--appsecret`：允许一次性运行时使用，但不要保存到仓库文件、日志或技能资源里。

绝不要打印 AppSecret、写入生成文件、提交到版本库，或放进最终回复。如果配置文件缺失，且用户在当前对话中提供 AppID/AppSecret，可以保存到当前用户的 `~/.config/wechat-mp/.env`；创建 `~/.config/wechat-mp` 时使用 `700` 权限，`.env` 文件使用 `600` 权限，并避免回显密钥。如果微信返回 IP 白名单错误，告诉用户将当前服务器 IP 加入微信公众号开发者设置中的 IP 白名单。

## 故障提示

当缺少 AppID/AppSecret、`access_token` 无效、接口权限不足、IP 白名单未配置，或微信 API 返回配置类错误时，最终回复必须提示用户打开微信开发者平台：`https://developers.weixin.qq.com/platform`。说明用户可以在这里获取或核对 AppID/AppSecret、配置服务器 IP 白名单、检查接口权限、账号认证状态和发布能力。

常见提示方式：

- 配置缺失：请到 `https://developers.weixin.qq.com/platform` 获取公众号 AppID/AppSecret，再写入 `~/.config/wechat-mp/.env`。
- `40164` 或 `invalid ip`：请到 `https://developers.weixin.qq.com/platform` 的公众号开发配置里，将当前服务器出口 IP 加入 IP 白名单。
- `40001`：请到 `https://developers.weixin.qq.com/platform` 核对 AppID/AppSecret 或 access token 所属账号。
- `48001`、`53504`、`53505` 或发布权限问题：请到 `https://developers.weixin.qq.com/platform` 检查接口权限、账号认证状态和发布相关能力。

## 命令行示例

创建 dry-run 载荷：

```bash
python scripts/wechat_mp_publish.py draft \
  --article ./article.html \
  --cover ./cover.jpg \
  --title "文章标题" \
  --dry-run
```

在公众号后台创建草稿：

```bash
python scripts/wechat_mp_publish.py draft \
  --article ./article.html \
  --cover ./cover.jpg \
  --title "文章标题"
```

发布已有草稿：

```bash
python scripts/wechat_mp_publish.py publish \
  --media-id MEDIA_ID \
  --confirm-publish
```

查询发布状态：

```bash
python scripts/wechat_mp_publish.py status --publish-id PUBLISH_ID
```

## 图片处理

- 除非提供 `--thumb-media-id`，否则封面图会作为永久图片素材上传，以获取 `thumb_media_id`。
- 正文中的封面图副本会在文内图片上传前移除；封面只通过 `thumb_media_id` 进入公众号文章，不要再把封面作为正文首图保留。
- 本地文内 `<img src="...">` 文件会通过微信文章图片接口上传，并改写为微信返回的图片 URL。
- 远程图片 URL 默认保持不变。提醒用户：微信文章内容可能拒绝非微信图片域名。
- 文章图片接口支持 1 MB 以下的 jpg/png。超大的文内图片需要压缩或替换后再重试。

## 标题处理

- 文章标题只通过草稿 payload 的 `title` 字段进入公众号后台。
- 正文中的主标题 `<h1>` 会在创建草稿前移除；保留正文的小标题、段落标题和后续结构标题。
- Markdown 文章使用一级标题推断 `title` 时，转换后的正文一级标题也会被移除，避免公众号页面重复显示标题。

## 代码块兼容

- 微信草稿可能会过滤或改写 `<pre>`、`<code>` 和 `white-space:pre-wrap`，导致代码块换行、缩进丢失。
- `scripts/wechat_mp_publish.py` 默认在读取 HTML、Markdown 或 JSON 文章后执行代码块归一化：保留原 `<pre style="...">` 中的大部分颜色、间距、字体样式，删除 `white-space` 依赖，并把代码文本转成显式 `<br>` 换行与 `&nbsp;` 空格。
- 不要手动关闭这一步。若草稿中代码块仍显示异常，先用 dry-run 输出检查最终 `content`，确认没有 `<pre`，再重新创建或更新草稿。

## 安全边界

- 除非用户明确要求这种方式，并接受手动登录或验证，否则不要用浏览器自动化登录 `mp.weixin.qq.com`。
- 不要绕过平台审核、二维码检查、安全提示、账号限制或内容规则。
- 将 `publish` 视为足够不可逆的操作，必须获得明确确认。创建草稿不需要同级别确认，但仍应尽可能先运行 dry-run。
- 如果请求涉及更新已有草稿，检查 `references/wechat_api.md`，并使用官方草稿更新接口，而不是创建重复草稿。

## 参考

当端点细节、错误码、权限或精确文章 JSON 结构很重要时，读取 `references/wechat_api.md`。
