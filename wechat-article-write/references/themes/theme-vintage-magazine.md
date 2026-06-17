# 主题：复古杂志

视觉定位：复古纸张底色、强标题、期刊眉标和叙事切片。强调纸媒质感、现场感和有节奏的视觉停顿，不绑定任何文章题材。

## 设计令牌

- 页面背景：`#efece5`
- 容器背景：`#fffaf2`
- 正文文字：`#2b2722`
- 弱化文字：`#756b61`
- 标题：`#17130f`
- 主强调色：`#b42318`
- 次强调色：`#7a5c2e`
- 柔和表面：`#f6efe3`
- 深色表面：`#231f1a`
- 边框：`#ddd2c2`
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
<body style="margin:0;padding:0;background:#efece5;color:#2b2722;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.92;">
  <section style="box-sizing:border-box;max-width:660px;margin:0 auto;padding:28px 18px 56px;background:#fffaf2;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 24px;border-radius:0;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:0;">
```

### 图片说明

```html
<p style="margin:0 0 24px;padding:0 0 0 12px;border-left:2px solid #b42318;font-size:13px;line-height:1.7;color:#756b61;">{{caption}}</p>
```

### 期刊眉标

```html
<section style="margin:0 0 18px;padding:0 0 12px;border-bottom:1px solid #ddd2c2;">
  <p style="margin:0;font-size:12px;line-height:1.5;color:#b42318;font-weight:800;letter-spacing:0;">{{kicker}}</p>
  <p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:#756b61;">{{date_or_issue}}</p>
</section>
```

### 标题和导语

```html
<section style="margin:0 0 28px;padding:18px 0 0;border-top:4px solid #17130f;">
  <h1 style="margin:0 0 14px;font-size:28px;line-height:1.34;font-weight:900;color:#17130f;letter-spacing:0;word-break:break-word;">{{title}}</h1>
  <p style="margin:0;font-size:17px;line-height:1.8;color:#5c5148;word-break:break-word;">{{deck}}</p>
</section>
```

### 章节标题

```html
<section style="margin:40px 0 18px;">
  <p style="margin:0 0 6px;font-size:36px;line-height:1;color:#b42318;font-weight:900;letter-spacing:0;">{{number}}</p>
  <h2 style="margin:0;padding:10px 0 0;border-top:1px solid #ddd2c2;font-size:22px;line-height:1.45;font-weight:900;color:#17130f;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 18px;font-size:16px;line-height:1.92;color:#2b2722;">{{text}}</p>
```

### 开场白

```html
<section style="margin:22px 0 30px;padding:18px 18px;background:#231f1a;">
  <p style="margin:0;font-size:18px;line-height:1.78;color:#fffaf2;font-weight:800;">{{lead}}</p>
</section>
```

### 叙事切片

```html
<section style="margin:22px 0 28px;padding:18px 0;border-top:1px solid #ddd2c2;border-bottom:1px solid #ddd2c2;">
  <p style="margin:0 0 8px;font-size:13px;color:#b42318;font-weight:800;">{{label}}</p>
  <p style="margin:0;font-size:16px;line-height:1.86;color:#3b342d;">{{text}}</p>
</section>
```

### 拉页引语

```html
<section style="margin:28px 0;padding:22px 18px;background:#f6efe3;border-left:5px solid #b42318;">
  <p style="margin:0;font-size:20px;line-height:1.72;color:#17130f;font-weight:900;">{{quote}}</p>
  <p style="margin:12px 0 0;font-size:13px;color:#756b61;">{{source}}</p>
</section>
```

### 叙事清单

```html
<section style="margin:20px 0 26px;padding:16px 18px;background:#f6efe3;border:1px solid #ddd2c2;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.82;color:#2b2722;">{{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.82;color:#2b2722;">{{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.82;color:#2b2722;">{{item3}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 24px;padding:16px;background:#231f1a;color:#f8ead9;border-radius:0;word-break:break-all;overflow-wrap:anywhere;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 参考资料组

搭配文末唯一的“参考资料”章节标题使用。多个来源连续列出，不要为每条资料重复写“参考资料”或“参考文章”标签。按来源数量复制或删除条目段落，最后一条使用 `margin:0`。

```html
<section style="margin:20px 0 26px;padding:15px 16px;background:#f6efe3;border:1px solid #ddd2c2;">
  <p style="margin:0 0 12px;font-size:15px;line-height:1.75;color:#17130f;font-weight:800;">{{label1}}<br><span style="font-size:13px;line-height:1.7;color:#7a5c2e;font-weight:400;word-break:break-all;">{{url1}}</span></p>
  <p style="margin:0;font-size:15px;line-height:1.75;color:#17130f;font-weight:800;">{{label2}}<br><span style="font-size:13px;line-height:1.7;color:#7a5c2e;font-weight:400;word-break:break-all;">{{url2}}</span></p>
</section>
```
