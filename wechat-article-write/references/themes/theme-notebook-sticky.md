# 主题：手账便签

视觉定位：暖纸页面、虚线边框、便签高亮和清单符号。强调亲近、轻松、可执行的手账质感，不绑定任何文章题材。

## 设计令牌

- 页面背景：`#f4f1ea`
- 容器背景：`#fffdf7`
- 正文文字：`#2f332f`
- 弱化文字：`#6c7268`
- 标题：`#1f241f`
- 主强调色：`#d97757`
- 次强调色：`#4f8f78`
- 柔和表面：`#f9f4e8`
- 便签表面：`#fff1b8`
- 深色表面：`#2b332f`
- 边框：`#ded5c6`
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
<body style="margin:0;padding:0;background:#f4f1ea;color:#2f332f;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.9;">
  <section style="box-sizing:border-box;max-width:660px;margin:0 auto;padding:28px 18px 54px;background:#fffdf7;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 26px;border-radius:12px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:12px;">
```

### 图片说明

```html
<p style="margin:0 0 22px;font-size:13px;line-height:1.68;color:#6c7268;text-align:center;">{{caption}}</p>
```

### 手账日期

```html
<section style="margin:0 0 18px;padding:12px 14px;background:#f9f4e8;border:1px dashed #c9bca9;border-radius:10px;">
  <p style="margin:0;font-size:13px;line-height:1.5;color:#d97757;font-weight:900;">{{label}}</p>
  <p style="margin:4px 0 0;font-size:13px;line-height:1.5;color:#6c7268;">{{date_or_context}}</p>
</section>
```

### 标题和导语

```html
<section style="margin:0 0 26px;">
  <h1 style="margin:0 0 12px;font-size:27px;line-height:1.36;font-weight:900;color:#1f241f;letter-spacing:0;word-break:break-word;">{{title}}</h1>
  <p style="margin:0;padding:0 0 0 14px;border-left:4px solid #d97757;font-size:16px;line-height:1.82;color:#5a6258;word-break:break-word;">{{deck}}</p>
</section>
```

### 章节标题

```html
<section style="margin:36px 0 18px;padding:12px 14px;background:#f9f4e8;border:1px dashed #c9bca9;border-radius:10px;">
  <p style="margin:0 0 5px;font-size:13px;color:#4f8f78;font-weight:900;">{{number}}</p>
  <h2 style="margin:0;font-size:21px;line-height:1.45;font-weight:900;color:#1f241f;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 16px;font-size:16px;line-height:1.9;color:#2f332f;">{{text}}</p>
```

### 便签

```html
<section style="margin:22px 0 28px;padding:18px;background:#fff1b8;border:1px solid #ead47b;border-radius:10px;">
  <p style="margin:0 0 8px;font-size:15px;color:#7c4a1e;font-weight:900;">{{label}}</p>
  <p style="margin:0;font-size:16px;line-height:1.78;color:#5c3b16;">{{text}}</p>
</section>
```

### 勾选清单

```html
<section style="margin:18px 0 24px;padding:16px 18px;background:#fffdf7;border:1px solid #ded5c6;border-radius:10px;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#2f332f;">□ {{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#2f332f;">□ {{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.8;color:#2f332f;">□ {{item3}}</p>
</section>
```

### 步骤卡

```html
<section style="margin:20px 0 26px;padding:18px;background:#eef7f2;border:1px solid #c8ded2;border-radius:10px;">
  <p style="margin:0 0 8px;font-size:15px;color:#2f6f58;font-weight:900;">{{step}}</p>
  <p style="margin:0;font-size:15px;line-height:1.78;color:#355046;">{{text}}</p>
</section>
```

### 复盘收束

```html
<section style="margin:28px 0;padding:18px;background:#2b332f;border-radius:10px;">
  <p style="margin:0;font-size:17px;line-height:1.74;color:#fffdf7;font-weight:800;">{{text}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:16px;background:#2b332f;color:#e8f5ec;border-radius:10px;word-break:break-all;overflow-wrap:anywhere;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 参考资料组

搭配文末唯一的“参考资料”章节标题使用。多个来源连续列出，不要为每条资料重复写“参考资料”或“参考文章”标签。按来源数量复制或删除条目段落，最后一条使用 `margin:0`。

```html
<section style="margin:18px 0 24px;padding:15px 16px;background:#f9f4e8;border:1px dashed #c9bca9;border-radius:10px;">
  <p style="margin:0 0 12px;font-size:15px;line-height:1.75;color:#1f241f;font-weight:800;">{{label1}}<br><span style="font-size:13px;line-height:1.68;color:#4f8f78;font-weight:400;word-break:break-all;">{{url1}}</span></p>
  <p style="margin:0;font-size:15px;line-height:1.75;color:#1f241f;font-weight:800;">{{label2}}<br><span style="font-size:13px;line-height:1.68;color:#4f8f78;font-weight:400;word-break:break-all;">{{url2}}</span></p>
</section>
```
