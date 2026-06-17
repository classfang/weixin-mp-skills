# 视觉风格索引

仅在选择公众号视觉风格时读取本文件。选定风格后，再加载对应的主题文件。下表中的文件和 HTML 用例路径均相对于本文件所在目录。

## 风格列表

| 风格 | 文件 | HTML 用例 | 视觉性格 | 版式特征 |
| --- | --- | --- | --- | --- |
| 冷感蓝图 | `theme-cool-blueprint.md` | `examples/cool-blueprint.html` | 清爽、理性、现代、冷色强调 | 蓝色编号、深色重点块、轻量边框卡片 |
| 原生蓝图 | `theme-native-blueprint.md` | `examples/native-blueprint.html` | 黑白理性、技术感、论证密度高 | 荧光标题、克制引用、深色流程代码框 |
| 极简墨色 | `theme-minimal-ink.md` | `examples/minimal-ink.html` | 克制、安静、文学感、高可读性 | 米白纸面、细分隔线、大段留白 |
| 暖白秩序 | `theme-warm-order.md` | `examples/warm-order.html` | 平静、可信、稳重、暖色点缀 | 暖色摘要、规则卡片、深色收束块 |
| 森绿编辑 | `theme-green-editorial.md` | `examples/green-editorial.html` | 清新、有组织、编辑部质感 | 绿色侧边线、浅绿卡片、柔和高亮框 |
| 复古杂志 | `theme-vintage-magazine.md` | `examples/vintage-magazine.html` | 纸媒感、叙事感、强标题、有现场感 | 期刊眉标、大号编号、拉页引语 |
| 蓝灰简报 | `theme-bluegray-brief.md` | `examples/bluegray-brief.html` | 冷静、紧凑、摘要感、信息密度高 | 页眉标签、关键数字、分隔式条目 |
| 黑金舞台 | `theme-noir-stage.md` | `examples/noir-stage.html` | 深色、高对比、仪式感、力量感 | 金色高光、暗色面板、舞台式重点块 |
| 手账便签 | `theme-notebook-sticky.md` | `examples/notebook-sticky.html` | 亲近、轻松、温和、可执行 | 虚线边框、便签高亮、勾选清单 |
| 青格笔记 | `theme-cyan-grid.md` | `examples/cyan-grid.html` | 清爽、学习感、网格纸、适合整理 | 网格纸背景、青色标题、引用块和表格 |

## 主题参数

生成公众号 HTML 时，可以用 `--theme <主题>` 指定视觉风格。参数值支持主题中文名、文件名 slug，或不带 `theme-` 前缀的短名。

| 参数值 | 主题 |
| --- | --- |
| `cool-blueprint` / `theme-cool-blueprint` / `冷感蓝图` | 冷感蓝图 |
| `native-blueprint` / `theme-native-blueprint` / `原生蓝图` | 原生蓝图 |
| `minimal-ink` / `theme-minimal-ink` / `极简墨色` | 极简墨色 |
| `warm-order` / `theme-warm-order` / `暖白秩序` | 暖白秩序 |
| `green-editorial` / `theme-green-editorial` / `森绿编辑` | 森绿编辑 |
| `vintage-magazine` / `theme-vintage-magazine` / `复古杂志` | 复古杂志 |
| `bluegray-brief` / `theme-bluegray-brief` / `蓝灰简报` | 蓝灰简报 |
| `noir-stage` / `theme-noir-stage` / `黑金舞台` | 黑金舞台 |
| `notebook-sticky` / `theme-notebook-sticky` / `手账便签` | 手账便签 |
| `cyan-grid` / `theme-cyan-grid` / `青格笔记` | 青格笔记 |

## 风格选择规则

- 视觉风格不绑定文章题材。技术、商业、观点、教程、复盘、故事类文章都可以自由选择任意风格。
- 如果用户明确指定风格名、明暗偏好、品牌气质或参考风格，优先按用户指定选择。
- 如果用户提供 `--theme <主题>`，优先按参数值选择对应主题；无法识别时，列出“主题参数”中的可用值并请用户确认。
- 如果用户没有指定，按视觉目标选择：清爽结构选冷感蓝图；黑白技术感选原生蓝图；安静慢读选极简墨色；稳重可信选暖白秩序；清新编辑感选森绿编辑；纸媒叙事选复古杂志；紧凑摘要选蓝灰简报；深色仪式感选黑金舞台；亲近手账感选手账便签；网格笔记感选青格笔记。
- 选择时优先判断阅读节奏、信息密度、明暗程度、装饰强度和情绪温度，而不是根据文章内容分类自动绑定主题。
- 同一篇文章可以换用不同风格。若没有强偏好，先给出一个推荐风格，并说明这是基于视觉气质而非题材类型。

## 风格应用

使用选定主题的页面外壳，然后用该主题的组件片段组织正文。保持语义结构简单，并将内联样式直接应用到元素上。

每个风格都有一个可直接在浏览器打开的 HTML 用例，位于 `references/themes/examples/`。打开 `references/themes/examples/index.html` 可以进入总览页；单个用例只用于预览排版效果，不作为发布内容模板。

如果某个主题组件不适合文章，可使用该主题的设计令牌调整间距和颜色，不要混用其他主题的组件。

对于发布就绪的微信公众号文章，图片组件中的 `{{image_src}}` 应使用 HTTPS 地址。正文链接不要用 `<a>`；在文末只出现一次“参考资料”章节标题，并使用所选主题的“参考资料组”组件把资料标题和完整 URL 都作为可见文本展示。本地图片路径只保留给预览版 HTML。
