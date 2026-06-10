# 主题：绿色编辑

适用于学习笔记、知识方法类文章、效率工作流、教育和实用框架。

## 设计令牌

- 页面背景：`#f3f7f4`
- 容器背景：`#ffffff`
- 正文文字：`#26332c`
- 弱化文字：`#5f6f66`
- 标题：`#102118`
- 主强调色：`#16815f`
- 次强调色：`#0f766e`
- 高亮色：`#f4c95d`
- 柔和表面：`#eef8f2`
- 深色表面：`#123026`
- 边框：`#d7e7dd`
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
<body style="margin:0;padding:0;background:#f3f7f4;color:#26332c;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.88;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:26px 16px 52px;background:#ffffff;">
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
<p style="margin:0 0 22px;font-size:13px;line-height:1.7;color:#5f6f66;text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="margin:0 0 14px;font-size:26px;line-height:1.38;font-weight:800;color:#102118;letter-spacing:0;word-break:break-word;">{{title}}</h1>
<p style="margin:0 0 24px;font-size:16px;color:#5f6f66;word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:36px 0 18px;padding:0 0 0 14px;border-left:4px solid #16815f;">
  <p style="margin:0 0 6px;font-size:13px;color:#16815f;font-weight:800;letter-spacing:0;">{{number}}</p>
  <h2 style="margin:0;font-size:22px;line-height:1.45;font-weight:800;color:#102118;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 16px;font-size:16px;color:#26332c;">{{text}}</p>
```

### 方法卡片

```html
<section style="margin:20px 0 24px;padding:18px;background:#eef8f2;border:1px solid #d7e7dd;border-radius:8px;">
  <p style="margin:0 0 8px;font-size:15px;color:#102118;font-weight:800;">{{title}}</p>
  <p style="margin:0;font-size:15px;color:#3c5146;">{{text}}</p>
</section>
```

### 高亮框

```html
<section style="margin:24px 0 30px;padding:18px;background:#fffbeb;border:1px solid #f4c95d;border-radius:8px;">
  <p style="margin:0;font-size:16px;color:#664d03;font-weight:700;">{{text}}</p>
</section>
```

### 检查清单

```html
<section style="margin:18px 0 24px;padding:18px;background:#f8fcf9;border:1px solid #d7e7dd;border-radius:8px;">
  <p style="margin:0 0 8px;font-size:15px;color:#26332c;">{{item}}</p>
</section>
```

### 多项列表

```html
<section style="margin:18px 0 24px;padding:18px;background:#f8fcf9;border:1px solid #d7e7dd;border-radius:8px;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#26332c;">{{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.8;color:#26332c;">{{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.8;color:#26332c;">{{item3}}</p>
</section>
```

### 代码块

```html
<pre style="margin:16px 0 22px;padding:16px;background:#123026;color:#dcfce7;border-radius:8px;white-space:pre-wrap;word-break:break-word;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code}}</pre>
```

### 参考文章

```html
<section style="margin:18px 0 24px;padding:15px 16px;background:#f8fcf9;border:1px solid #d7e7dd;border-radius:8px;">
  <p style="margin:0 0 6px;font-size:13px;color:#16815f;font-weight:800;">参考文章</p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.7;color:#102118;font-weight:700;">{{label}}</p>
  <p style="margin:0;font-size:13px;line-height:1.65;color:#0f766e;word-break:break-all;">{{url}}</p>
</section>
```
