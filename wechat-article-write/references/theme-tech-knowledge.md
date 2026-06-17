# 主题：科技知识

适用于 AI 工具、架构、开发者工作流、技术教程和系统设计文章。

## 设计令牌

- 页面背景：`#f6f8fb`
- 容器背景：`#ffffff`
- 正文文字：`#1f2937`
- 弱化文字：`#4b5563`
- 标题：`#111827`
- 主强调色：`#0ea5e9`
- 次强调色：`#22c55e`
- 深色表面：`#0f172a`
- 代码文字：`#dbeafe`
- 边框：`#e5e7eb`
- 字体栈：`-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif`
- 等宽字体栈：`'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace`

## 页面外壳

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
</head>
<body style="margin:0;padding:0;background:#f6f8fb;color:#1f2937;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.85;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:24px 16px 48px;background:#ffffff;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 28px;border-radius:8px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:8px 0 10px;border-radius:8px;">
```

### 图片说明

```html
<p style="margin:0 0 22px;font-size:13px;line-height:1.7;color:#6b7280;text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="margin:0 0 14px;font-size:26px;line-height:1.35;font-weight:800;color:#111827;letter-spacing:0;text-align:left;word-break:break-word;">{{title}}</h1>
<p style="margin:0 0 22px;font-size:16px;color:#4b5563;word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:34px 0 18px;">
  <p style="margin:0 0 8px;font-size:14px;color:#0ea5e9;font-weight:800;letter-spacing:0;">{{number}}</p>
  <h2 style="margin:0 0 18px;font-size:22px;line-height:1.45;font-weight:800;color:#111827;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 16px;font-size:16px;color:#374151;">{{text}}</p>
```

### 开场引用

```html
<section style="margin:26px 0;padding:18px 18px;border-left:4px solid #0ea5e9;background:#f0f9ff;border-radius:6px;">
  <p style="margin:0 0 10px;font-size:16px;color:#334155;">{{line1}}</p>
  <p style="margin:0;font-size:16px;color:#0f172a;font-weight:700;">{{line2}}</p>
</section>
```

### 核心要点

```html
<section style="margin:24px 0 32px;padding:18px;background:#111827;border-radius:8px;color:#f9fafb;">
  <p style="margin:0 0 12px;font-size:16px;font-weight:700;color:#ffffff;">{{label}}</p>
  <p style="margin:0 0 8px;font-size:16px;color:#e5e7eb;">{{point1}}</p>
  <p style="margin:0;font-size:16px;color:#e5e7eb;">{{point2}}</p>
</section>
```

### 列表卡片

```html
<section style="margin:18px 0 22px;padding:18px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;">
  <p style="margin:0 0 8px;font-size:15px;color:#374151;">{{item}}</p>
</section>
```

### 多项列表

```html
<section style="margin:18px 0 24px;padding:18px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#374151;">{{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#374151;">{{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.8;color:#374151;">{{item3}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:16px;background:#0f172a;color:#dbeafe;border-radius:8px;word-break:break-all;overflow-wrap:anywhere;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 参考文章

```html
<section style="margin:18px 0 24px;padding:14px 16px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;">
  <p style="margin:0 0 6px;font-size:13px;color:#0ea5e9;font-weight:800;">参考文章</p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.7;color:#111827;font-weight:700;">{{label}}</p>
  <p style="margin:0;font-size:13px;line-height:1.65;color:#2563eb;word-break:break-all;">{{url}}</p>
</section>
```
