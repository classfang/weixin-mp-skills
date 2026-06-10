# 主题：极简墨色

适用于随笔、反思性技术写作、观点文章、个人分析和深度阅读。

## 设计令牌

- 页面背景：`#f7f5f0`
- 容器背景：`#fffdf8`
- 正文文字：`#2f2f2f`
- 弱化文字：`#6b6258`
- 标题：`#171717`
- 强调色：`#8b5e34`
- 柔和表面：`#f3efe6`
- 深色表面：`#27231f`
- 边框：`#e8dfd2`
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
<body style="margin:0;padding:0;background:#f7f5f0;color:#2f2f2f;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.95;">
  <section style="box-sizing:border-box;max-width:660px;margin:0 auto;padding:30px 18px 54px;background:#fffdf8;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 30px;border-radius:4px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:4px;">
```

### 图片说明

```html
<p style="margin:0 0 24px;font-size:13px;line-height:1.75;color:#7c7167;text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="margin:0 0 16px;font-size:26px;line-height:1.42;font-weight:800;color:#171717;letter-spacing:0;word-break:break-word;">{{title}}</h1>
<p style="margin:0 0 28px;font-size:16px;color:#6b6258;word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:38px 0 20px;padding:0 0 10px;border-bottom:1px solid #e8dfd2;">
  <p style="margin:0 0 6px;font-size:13px;color:#8b5e34;font-weight:700;letter-spacing:0;">{{number}}</p>
  <h2 style="margin:0;font-size:21px;line-height:1.5;font-weight:800;color:#171717;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 18px;font-size:16px;color:#2f2f2f;">{{text}}</p>
```

### 提炼引用

```html
<section style="margin:28px 0;padding:20px 20px;background:#f3efe6;border-radius:6px;">
  <p style="margin:0;font-size:18px;line-height:1.8;color:#171717;font-weight:700;">{{quote}}</p>
</section>
```

### 轻提示

```html
<section style="margin:22px 0 28px;padding:16px 18px;border-left:3px solid #8b5e34;background:#fbf8f1;">
  <p style="margin:0;font-size:15px;color:#4b4036;">{{text}}</p>
</section>
```

### 列表卡片

```html
<section style="margin:18px 0 24px;padding:16px 18px;background:#fbf8f1;border:1px solid #e8dfd2;border-radius:6px;">
  <p style="margin:0 0 8px;font-size:15px;color:#3f3a34;">{{item}}</p>
</section>
```

### 多项列表

```html
<section style="margin:18px 0 26px;padding:16px 18px;background:#fbf8f1;border:1px solid #e8dfd2;border-radius:6px;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.85;color:#3f3a34;">{{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.85;color:#3f3a34;">{{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.85;color:#3f3a34;">{{item3}}</p>
</section>
```

### 代码块

```html
<pre style="margin:16px 0 24px;padding:16px;background:#27231f;color:#f5efe7;border-radius:6px;white-space:pre-wrap;word-break:break-word;font-size:14px;line-height:1.78;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code}}</pre>
```

### 参考文章

```html
<section style="margin:20px 0 26px;padding:15px 18px;background:#fbf8f1;border:1px solid #e8dfd2;border-radius:6px;">
  <p style="margin:0 0 6px;font-size:13px;color:#8b5e34;font-weight:700;">参考文章</p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:#171717;font-weight:700;">{{label}}</p>
  <p style="margin:0;font-size:13px;line-height:1.7;color:#6b6258;word-break:break-all;">{{url}}</p>
</section>
```
