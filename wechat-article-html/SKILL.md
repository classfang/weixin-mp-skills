---
name: wechat-article-html
description: 为微信公众号创建可直接粘贴的图文 HTML，包含内联样式、可选主题、可发布的 HTTPS 图片地址，并默认避免正文 `<a>` 超链接。当 Codex 需要把 Markdown、纯文本、草稿、大纲或长文转换成可在浏览器打开、复制并粘贴到微信公众号编辑器的富文本 HTML 时使用；支持将链接改写为“参考文章/参考链接”可见文本块、本地预览图片、远程图片托管，以及 references/ 中的多套主题模板。
---

# 微信公众号图文 HTML

## 用途

创建一个独立的 `.html` 文件。用户可以在浏览器里打开它，复制渲染后的正文，再粘贴到微信公众号富文本编辑器中。优先使用简单 HTML 结构和内联样式，以提高通过公众号编辑器过滤的概率。

## 工作流

1. 规范文章：
   - 保留用户原意和章节顺序。
   - 将 Markdown 标题、列表、引用、代码块、链接和图片转换成明确的 HTML。
   - 将 Markdown/HTML 中的链接默认改写为“参考资料”展示块，保留标题和 URL 可见文本。
   - 确保标题、副标题/导语和章节编号在手机端清晰可读。
2. 选择主题：
   - 如果用户指定主题，加载对应主题参考文件。
   - 如果用户未指定主题，加载 `references/themes-index.md` 并选择最合适的主题。
   - 除非用户要求比较多个主题，否则只加载已选主题文件。
3. 构建 HTML：
   - 使用一个自包含的 `.html` 文件，包含 UTF-8 meta 标签和移动端 viewport。
   - 将样式直接写到内容元素的 `style` 属性里。避免外部 CSS、CSS class、脚本、iframe、表单、事件处理器和远程字体。
   - 使用居中的内容容器，宽度约 640-680px。
   - 主要使用 `section`、`p`、`h1`、`h2`、`img`、`pre` 和 `strong` 标签。
   - 默认不要生成正文 `<a>` 标签，因为公众号发布后正文超链接容易被过滤或丢失。
   - 对外部资料使用“参考资料”块：一行标题/来源，一行完整 URL。URL 必须是可见文本，使用 `word-break:break-all`，方便读者复制。
   - 只有当用户明确要求保留浏览器预览用可点击链接时，才生成 `<a href="...">`，并说明该版本不适合作为公众号发布 HTML。
   - `<pre>` 中的代码和原始 HTML 必须转义。
4. 处理图片：
   - 如果用户会直接粘贴到微信公众号编辑器，优先使用可发布的 HTTPS 图片地址。本地相对路径只适合本地预览。
   - 如果已有服务器或静态托管路径，将生成图片或用户提供的图片上传到可公网访问的目录，并把 `img src` 改写成标准 `443` 端口上的 HTTPS URL。
   - 使用主题图片片段中的 `{{image_src}}` 占位值；本地相对路径仅保留给预览版本。
   - 不要在最终公众号图片地址里使用本地路径、`file://`、私有 IP、纯 `http` 或 `:8088` 等非标准端口；浏览器可能能加载，但微信后端图片抓取器可能失败。
   - 使用自定义 Nginx 图片托管时，尽量通过已有 HTTPS server block 暴露资源，例如 `https://example.com/wechat-assets/article-slug/image.png`。可以保留单独调试端口，但最终文章 HTML 不要使用调试端口。
   - 图片标签保持简单：全宽、`height:auto`、可选小圆角、描述性的 `alt`。
5. 完成前校验：
   - 确认输出文件存在。
   - 预览版本要检查所有本地图片存在；发布版本要检查所有远程图片 URL 返回 `200 OK` 且 `Content-Type` 为图片类型。
   - 快速检查 HTML，避免未转义的 `<script`、`onclick`、`class=`、`<a href`、外部样式表或损坏的相对路径。
   - 对微信公众号发布版本，确认 HTML 中没有 `file://`、本地相对图片路径、纯 `http` 图片 URL、私有 IP 图片 URL 或带非标准端口的图片 URL。
   - 如果浏览器工具可用且有帮助，打开文件并目检渲染后的复制界面。

## 远程图片托管

当用户希望直接复制粘贴到微信公众号，并且有 SSH/Nginx 托管环境时：

1. 将图片上传到服务器上稳定的静态目录，例如 `/var/www/wechat-assets/<article-slug>/`。
2. 配置 Nginx，让该目录通过已有 HTTPS 域名的 `443` 端口访问，推荐路径形如 `/wechat-assets/<article-slug>/`。
3. 在服务器外部用 `curl -I https://domain/wechat-assets/<article-slug>/<file>.png` 校验每张图片；期望返回 `200 OK`，且 `Content-Type` 为 `image/png` 或对应图片类型。
4. 生成一个发布就绪的 HTML/Markdown 版本，图片引用使用这些 HTTPS URL。只有在对用户有帮助时才保留本地预览版本。
5. 告诉用户哪个文件是发布就绪的复制源，并列出公开图片基础 URL。

## 输出

除非用户指定其他位置，否则把面向用户的文件放在工作区 `outputs/` 目录。使用清晰文件名，例如：

```text
outputs/wechat-article.html
outputs/wechat-article-cover.png
```

最终回复中链接 HTML 文件和所有复制出的素材。如果创建了带远程图片的发布就绪版本，把它作为首选文件，并说明用户应在浏览器打开它，选中渲染后的文章，复制后粘贴到微信公众号编辑器。

## 主题参考

- `references/themes-index.md`：主题选择指南。
- `references/theme-tech-knowledge.md`：技术文章、AI 工具、开发者工作流。
- `references/theme-minimal-ink.md`：深度阅读、随笔、观点文章。
- `references/theme-warm-business.md`：商业、产品、战略、职场文章。
- `references/theme-green-editorial.md`：知识方法、效率、教育类文章。

主题文件定义颜色、排版、间距和可复用 HTML 片段。根据文章调整片段，而不是机械复制每个组件。

## 微信公众号兼容规则

- 从浏览器复制渲染后的富文本，不要复制 HTML 源码。
- 样式保持内联且保守。
- 不要依赖 `<style>`、`<script>`、复杂选择器、自定义字体或 JavaScript 交互。
- 正文默认不要依赖 `<a>` 超链接。把外部资料做成“参考资料”文本块，显示标题和完整 URL。
- 除非用户明确需要表格，否则避免大量表格布局。
- 避免过小文字、密集多列布局、宽于手机屏幕的固定宽度，以及承载关键信息的纯装饰元素。
- 将代码块和长 URL 视为手机端溢出风险；使用 `white-space:pre-wrap` 和 `word-break:break-word`。
