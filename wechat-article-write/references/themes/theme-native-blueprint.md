# 主题：原生蓝图

适用于 AI-Native、软件工程范式、技术战略、架构方法论和长篇技术分析文章。主题采用黑白正文基底、浅蓝荧光标题、克制引用块和深色代码框，适合承载结构清晰、论证密度较高的技术长文。

## 设计令牌

- 页面背景：`#f6f8fa`
- 容器背景：`#ffffff`
- 正文文字：`#000000`
- 弱化文字：`#666666`
- 标题：`#000000`
- 主强调色：`#70bcea`
- 高亮底色：`#e7f7fc`
- 引用表面：`#f2f2f2`
- 代码背景：`#282c34`
- 代码文字：`#abb2bf`
- 边框：`rgba(0,0,0,0.4)`
- 柔和边框：`#e5e7eb`
- 字体栈：`Optima,'Microsoft YaHei','PingFang SC','Hiragino Sans GB',serif`
- 等宽字体栈：`Consolas,Monaco,Menlo,monospace`

## 页面外壳

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
</head>
<body style="margin:0;padding:0;background:#f6f8fa;color:#000000;font-family:Optima,'Microsoft YaHei','PingFang SC','Hiragino Sans GB',serif;line-height:1.8;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:24px 20px 52px;background:#ffffff;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 28px;border-radius:6px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:6px;">
```

### 图片说明

```html
<p style="margin:5px 0 22px;font-size:14px;line-height:1.5;color:#888888;text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="margin:30px 0 15px;font-size:24px;line-height:1.5;font-weight:800;color:#000000;letter-spacing:0;text-align:left;word-break:break-word;">{{title}}</h1>
<p style="margin:0 0 22px;padding:8px 0;font-size:16px;line-height:1.8;color:#666666;letter-spacing:0;text-align:left;word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:30px 0 15px;line-height:1.5;text-align:left;">
  <h2 style="display:inline;margin:0;padding:0 10px 0 0;font-size:22px;line-height:1.8;font-weight:800;color:#70bcea;letter-spacing:0;background:linear-gradient(0deg,#e7f7fc 40%,transparent 40%);">{{heading}}</h2>
</section>
```

### 小节标题

```html
<h3 style="margin:30px 0 15px;font-size:20px;line-height:1.5;font-weight:800;color:#000000;letter-spacing:0;text-align:left;">{{heading}}</h3>
```

### 段落

```html
<p style="margin:0;padding:8px 0;font-size:16px;line-height:1.8;color:#000000;letter-spacing:0;text-align:left;text-indent:0;">{{text}}</p>
```

### 引用块

```html
<section style="margin:20px 0;padding:10px 10px 10px 20px;background:#f2f2f2;border-left:3px solid rgba(0,0,0,0.4);overflow-wrap:anywhere;">
  <p style="margin:0;padding:8px 0;font-size:16px;line-height:1.8;color:#000000;font-style:italic;">{{quote}}</p>
</section>
```

### 分隔线

```html
<section style="margin:10px 0;height:1px;border-top:1px solid #000000;font-size:0;line-height:0;">&nbsp;</section>
```

### 概念卡片

```html
<section style="margin:16px 0 20px;padding:14px 16px;background:#f8f8f8;border:1px solid #e5e7eb;border-radius:6px;">
  <p style="margin:0 0 8px;font-size:16px;line-height:1.8;color:#000000;font-weight:800;">{{title}}</p>
  <p style="margin:0;font-size:16px;line-height:1.8;color:#000000;">{{text}}</p>
</section>
```

### 多项列表

```html
<section style="margin:8px 0 18px;padding:0 0 0 25px;color:#000000;">
  <p style="margin:5px 0;font-size:16px;line-height:1.8;color:#010101;">{{item1}}</p>
  <p style="margin:5px 0;font-size:16px;line-height:1.8;color:#010101;">{{item2}}</p>
  <p style="margin:5px 0;font-size:16px;line-height:1.8;color:#010101;">{{item3}}</p>
</section>
```

### 流程代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:10px 0;padding:16px 16px 15px;background:#282c34;color:#abb2bf;border-radius:5px;box-shadow:rgba(0,0,0,0.55) 0 2px 10px;word-break:break-all;overflow-wrap:anywhere;font-size:12px;line-height:1.8;font-family:Consolas,Monaco,Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 关键判断

```html
<section style="margin:20px 0;padding:14px 16px;background:#e7f7fc;border-left:4px solid #70bcea;border-radius:5px;">
  <p style="margin:0;font-size:16px;line-height:1.8;color:#000000;font-weight:800;">{{text}}</p>
</section>
```

### 参考文章

```html
<section style="margin:18px 0 24px;padding:14px 16px;background:#f8f8f8;border:1px solid #e5e7eb;border-radius:6px;">
  <p style="margin:0 0 6px;font-size:13px;color:#70bcea;font-weight:800;">参考文章</p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.7;color:#000000;font-weight:700;">{{label}}</p>
  <p style="margin:0;font-size:13px;line-height:1.65;color:#666666;word-break:break-all;">{{url}}</p>
</section>
```
