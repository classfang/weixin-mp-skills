# 📮 微信公众号运维 Skills

这是一个面向微信公众号内容生产和运维的 Codex Skill 合集。它把常见的公众号工作流沉淀成三个可复用节点：文章创作、文章配图、文章发布。

推荐优先在 Codex 中使用这些技能。Codex 会读取每个技能目录中的 `SKILL.md` 元数据，并在任务匹配时自动选择合适的技能；你也可以在提示词里显式使用 `$技能名` 调用。

## 🧩 技能列表

| 技能 | 用途 |
| --- | --- |
| `$wechat-article-write` | 文章创作节点。负责选题理解、标题大纲、正文写作、主题匹配、封面图和文内配图 prompt；需要时可输出公众号可粘贴 HTML。 |
| `$wechat-article-image` | 文章配图节点。负责微信公众号封面图、头图和文内配图，默认偏好 2.35:1 宽幅封面和“重图轻标题”的知识媒体风格。 |
| `$wechat-article-publish` | 文章发布节点。通过微信公众号官方服务端 API 上传本地图文素材，默认创建公众号草稿，并在明确确认后提交发布或查询发布状态。 |

## 🧭 适合的工作流

- 从选题、草稿或大纲创作一篇公众号文章，并匹配主题与配图 prompt。
- 为文章生成封面图、头图或文内配图。
- 将本地 HTML、Markdown 或 JSON 文章推送到公众号后台草稿箱。
- 将公众号发布流程中的注意事项、凭据读取方式、图片限制和错误处理交给 Codex 统一执行。

## ⚙️ 安装到 Codex

### 📥 1. 克隆仓库

```bash
git clone https://github.com/<your-org-or-user>/weixin-mp-skills.git
cd weixin-mp-skills
```

如果你是直接下载压缩包，解压后进入仓库根目录即可。

### 📁 2. 创建本地技能目录

```bash
mkdir -p ~/.codex/skills
```

### 📦 3. 拷贝技能目录

```bash
cp -R wechat-article-write ~/.codex/skills/
cp -R wechat-article-image ~/.codex/skills/
cp -R wechat-article-publish ~/.codex/skills/
```

也可以一次性拷贝：

```bash
cp -R wechat-article-write wechat-article-image wechat-article-publish ~/.codex/skills/
```

### 🔄 4. 重启或刷新 Codex

重新打开 Codex，或开启一个新的 Codex 会话。之后可以在任务里直接写技能名，例如：

```text
使用 $wechat-article-write 根据这个选题创作一篇公众号文章，并给出主题匹配和配图 prompt。
```

```text
使用 $wechat-article-image 为这篇文章生成一张公众号封面图。
```

```text
使用 $wechat-article-publish 将 ./outputs/article.html 创建为公众号草稿。
```

如果你的 Codex 版本没有在 `~/.codex/skills` 中识别到这些技能，请检查 Codex 的技能列表或当前版本文档；部分版本也支持 open agent skills 标准目录，例如 `~/.agents/skills`。

## 💡 使用建议

### 📝 文章创作

把文章草稿、Markdown 文件或大纲交给 Codex，并说明目标：

```text
使用 $wechat-article-write 处理 ./draft.md，改写成一篇适合微信公众号发布的文章，并规划封面图和文内配图 prompt。
```

技能会优先生成可继续编辑的 Markdown 正文、推荐标题、摘要导语、主题匹配和配图 prompt。只有在你要求公众号 HTML 时，才额外生成可复制到编辑器的自包含 HTML。

### 🎨 封面和配图

给 Codex 文章主题、标题、摘要、正文，或文章创作节点产出的配图 prompt：

```text
使用 $wechat-article-image 给《AI 工作流反推提示词》生成一张微信公众号封面图。
```

技能默认会控制画面比例、标题占比、中文字体质感和知识媒体风格，避免只做大字海报。

### 🚀 草稿和发布

发布相关技能默认先创建草稿，不会擅自发布。正式发布前需要你明确确认：

```text
使用 $wechat-article-publish 将 ./outputs/article.html 和 ./outputs/cover.jpg 创建为公众号草稿。
```

发布技能会读取本地配置文件或环境变量中的公众号凭据。推荐把凭据放在：

```text
~/.config/wechat-mp/.env
```

示例字段：

```bash
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
```

## 🤝 贡献

欢迎提交 PR 完善现有 skill，或新增更多公众号运维相关 skill。建议在 PR 中说明适用场景、触发方式、输入输出示例，以及是否依赖脚本、外部服务或凭据。
