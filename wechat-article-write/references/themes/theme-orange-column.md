# 主题：橙点专栏

视觉定位：复刻参考文章 `js_content` 主体排版。一模一样使用原文的高频 inline style：正文段落、橙色章节标题、图片容器、图片样式和少量左边线强调块。不要再额外设计卡片、圆角面板、深色数据块或延展配色。

## 原文样式指纹

参考文章主体中最常出现的样式如下：

- 正文段落：出现 57 次。
- 图片容器：出现 20 次。
- 橙色章节标题：出现 2 次。
- 图片标签：出现 21 次。

复制这个主题时，优先使用这些组件，而不是把它改造成常规知识媒体卡片风。

## 设计令牌

- 页面背景：`#ffffff`
- 容器背景：`#ffffff`
- 正文文字：`rgb(34, 34, 34)`
- 标题强调色：`rgb(253, 70, 6)`
- 招聘区正文文字：`rgb(78, 79, 80)`
- 招聘区强调文字：`rgb(0, 0, 0)`
- 招聘区红色文字：`rgb(217, 33, 66)`
- 引用边框：`rgb(216, 216, 216)`
- 正文字号：`15px`
- 正文行高：`25px`
- 章节字号：`21px`
- 章节行高：`29px`
- 正文字体栈：`system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif`
- 招聘区字体栈：`system-ui,-apple-system,BlinkMacSystemFont,"Helvetica Neue","PingFang SC","Hiragino Sans GB","Microsoft YaHei UI","Microsoft YaHei",Arial,sans-serif`

## 页面外壳

页面外壳仅用于本地预览。公众号正文中应直接使用下方组件片段；原文主体本身不依赖额外卡片容器。

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
</head>
<body style="margin:0;padding:0;background:#ffffff;color:rgb(34, 34, 34);font-family:system-ui,-apple-system,&quot;Segoe UI&quot;,Roboto,&quot;Helvetica Neue&quot;,Arial,sans-serif;">
  <section style="box-sizing:border-box;max-width:784px;margin:0 auto;padding:0;background:#ffffff;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 正文段落

原文主体最高频组件。普通段落、口语解释、案例描述和结论推进都使用这一段。

```html
<section style="margin: 27px 0px;padding: 0px 15px;font-size: 15px;color: rgb(34, 34, 34);text-align: justify;line-height: 25px;font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif;"><span leaf="">{{text}}</span></section>
```

### 橙色章节标题

原文中用于“安装到 Codex”“马尾辫的适用场景有哪些”这类一级章节。

```html
<section style="font-weight: 600;font-size: 21px;color: rgb(253, 70, 6);text-align: justify;line-height: 29px;margin: 65px 0px 27px;padding: 0px 15px;font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif;"><span leaf="">{{heading}}</span></section>
```

### 图片容器

原文截图、说明图和流程图都使用这个外层容器。图片紧跟段落之后时，图片下方不额外留白；下一段正文用自己的 `margin: 27px 0px` 拉开距离。

```html
<section style="padding: 0px 15px;margin: 27px 0px 0px;text-align: center;box-sizing: border-box;font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif;" nodeleaf=""><img src="{{image_src}}" alt="{{alt}}" style="width: 754px;font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif;" /></section>
```

### 左边线强调块

原文中少量使用的强调块，适合放一句关键判断或提示。它不是卡片，不要加背景色和圆角。

```html
<section style="margin: 26px 0px;padding: 0px 15px 0px 14px;border-left-width: 4px;border-left-style: solid;border-left-color: rgb(216, 216, 216);font-size: 15px;line-height: 23px;font-weight: 600;color: rgb(34, 34, 34);font-family: system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif;"><span leaf="">{{text}}</span></section>
```

### 招聘标题

原文尾部招聘区的标题样式。只有确实需要复刻尾部招聘/公告块时使用。

```html
<section style="margin: 24px 16px 30px;padding: 0px;outline: 0px;max-width: 100%;font-style: normal;font-variant-ligatures: normal;font-variant-caps: normal;orphans: 2;text-indent: 0px;text-transform: none;widows: 2;word-spacing: 0px;-webkit-text-stroke-width: 0px;white-space: normal;text-decoration-thickness: initial;text-decoration-style: initial;text-decoration-color: initial;background-color: rgb(255, 255, 255);letter-spacing: 0.578px;caret-color: rgb(0, 0, 0);font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, system-ui, &quot;Helvetica Neue&quot;, Helvetica, Tahoma, Arial, &quot;Heiti SC&quot;, STHeiti, SimHei, sans-serif;font-size: 20px;color: rgb(14, 14, 14);line-height: 1.5;font-weight: bold;text-align: center;box-sizing: border-box !important;overflow-wrap: break-word !important;"><span style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;color: rgb(34, 34, 34);box-sizing: border-box !important;overflow-wrap: break-word !important;"><span leaf="" style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><span textstyle="" style="font-size: 15px;letter-spacing: normal;">{{heading}}</span></span></span></section>
```

### 招聘正文

原文尾部招聘/公告区正文。可配合 `strong` 和红色 span 还原强调文字。

```html
<section style="margin: 24px 16px 30px;padding: 0px;outline: 0px;max-width: 100%;font-style: normal;font-variant-ligatures: normal;font-variant-caps: normal;font-weight: 400;letter-spacing: 0.544px;orphans: 2;text-indent: 0px;text-transform: none;widows: 2;word-spacing: 0px;-webkit-text-stroke-width: 0px;white-space: normal;text-decoration-thickness: initial;text-decoration-style: initial;text-decoration-color: initial;background-color: rgb(255, 255, 255);caret-color: rgb(0, 0, 0);text-align: start;font-family: system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif;font-size: 15px;color: rgb(78, 79, 80);line-height: 1.75;box-sizing: border-box !important;overflow-wrap: break-word !important;">{{content}}</section>
```

招聘正文中的强强调：

```html
<span style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;color: rgb(0, 0, 0);box-sizing: border-box !important;overflow-wrap: break-word !important;"><strong style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;"><span leaf="" style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;box-sizing: border-box !important;overflow-wrap: break-word !important;">{{text}}</span></strong></span>
```

招聘正文中的红色强调：

```html
<span style="margin-bottom: 0px;padding: 0px;outline: 0px;max-width: 100%;color: rgb(217, 33, 66);box-sizing: border-box !important;overflow-wrap: break-word !important;">{{text}}</span>
```

## 使用规则

- 普通正文不要改成 `<p>`，使用原文的 `<section><span leaf="">...</span></section>`。
- 章节标题不要加编号、边框、背景、圆角或额外英文标签。
- 图片不要加圆角、阴影、图注卡片或 `max-width` 扩展样式；如果本地预览需要响应式，可只在预览外壳控制容器宽度。
- 代码、命令和列表在原文中通常也是正文段落样式，不单独做深色代码块。
- 若不是尾部招聘/公告内容，不使用招聘区组件。
