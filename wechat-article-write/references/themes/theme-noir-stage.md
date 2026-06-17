# 主题：黑金舞台

视觉定位：深色页面、高对比文字、金色高光和聚光灯式重点块。强调仪式感、力量感和强烈视觉停顿，不绑定任何文章题材。

## 设计令牌

- 页面背景：`#07080c`
- 容器背景：`#10131a`
- 正文文字：`#e8edf5`
- 弱化文字：`#a6b0c2`
- 标题：`#ffffff`
- 主强调色：`#f4c95d`
- 次强调色：`#38bdf8`
- 柔和表面：`#171b24`
- 深色表面：`#07080c`
- 边框：`#2a3140`
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
<body style="margin:0;padding:0;background:#07080c;color:#e8edf5;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.82;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:26px 16px 54px;background:#10131a;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 24px;border-radius:10px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:10px;">
```

### 图片说明

```html
<p style="margin:0 0 24px;font-size:13px;line-height:1.65;color:#a6b0c2;text-align:center;">{{caption}}</p>
```

### 高光徽章

```html
<section style="margin:0 0 18px;padding:12px 14px;background:#171b24;border:1px solid #2a3140;border-radius:10px;">
  <p style="margin:0;font-size:12px;line-height:1.5;color:#f4c95d;font-weight:900;">{{label}}</p>
  <p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:#a6b0c2;">{{date_or_version}}</p>
</section>
```

### 标题和导语

```html
<section style="margin:0 0 28px;padding:22px 18px;background:#07080c;border:1px solid #2a3140;border-radius:12px;">
  <p style="margin:0 0 10px;font-size:13px;color:#f4c95d;font-weight:900;">{{kicker}}</p>
  <h1 style="margin:0 0 14px;font-size:28px;line-height:1.32;font-weight:900;color:#ffffff;letter-spacing:0;word-break:break-word;">{{title}}</h1>
  <p style="margin:0;font-size:16px;line-height:1.74;color:#cbd5e1;word-break:break-word;">{{deck}}</p>
</section>
```

### 章节标题

```html
<section style="margin:38px 0 18px;">
  <p style="margin:0 0 8px;font-size:13px;color:#38bdf8;font-weight:900;">{{number}}</p>
  <h2 style="margin:0;padding:0 0 12px;border-bottom:1px solid #2a3140;font-size:22px;line-height:1.42;font-weight:900;color:#ffffff;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 16px;font-size:16px;line-height:1.82;color:#e8edf5;">{{text}}</p>
```

### 舞台重点

```html
<section style="margin:24px 0 30px;padding:20px;background:#171b24;border:1px solid #3a4254;border-radius:12px;">
  <p style="margin:0 0 10px;font-size:13px;color:#f4c95d;font-weight:900;">{{label}}</p>
  <p style="margin:0;font-size:20px;line-height:1.6;color:#ffffff;font-weight:900;">{{text}}</p>
</section>
```

### 功能亮点

```html
<section style="margin:20px 0 26px;padding:18px;background:#07080c;border:1px solid #2a3140;border-radius:10px;">
  <p style="margin:0 0 8px;font-size:16px;color:#ffffff;font-weight:900;">{{title}}</p>
  <p style="margin:0;font-size:15px;line-height:1.76;color:#cbd5e1;">{{text}}</p>
</section>
```

### 节奏条目

```html
<section style="margin:18px 0 24px;padding:0;border:1px solid #2a3140;border-radius:10px;overflow:hidden;">
  <p style="margin:0;padding:13px 14px;background:#171b24;font-size:15px;line-height:1.72;color:#e8edf5;">{{item1}}</p>
  <p style="margin:0;padding:13px 14px;border-top:1px solid #2a3140;font-size:15px;line-height:1.72;color:#e8edf5;">{{item2}}</p>
  <p style="margin:0;padding:13px 14px;border-top:1px solid #2a3140;font-size:15px;line-height:1.72;color:#e8edf5;">{{item3}}</p>
</section>
```

### 金色收束

```html
<section style="margin:28px 0;padding:18px;background:#f4c95d;border-radius:10px;">
  <p style="margin:0;font-size:17px;line-height:1.72;color:#17130f;font-weight:900;">{{text}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:16px;background:#07080c;color:#bae6fd;border:1px solid #2a3140;border-radius:10px;word-break:break-all;overflow-wrap:anywhere;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 参考资料组

搭配文末唯一的“参考资料”章节标题使用。多个来源连续列出，不要为每条资料重复写“参考资料”或“参考文章”标签。按来源数量复制或删除条目段落，最后一条使用 `margin:0`。

```html
<section style="margin:18px 0 24px;padding:15px 16px;background:#171b24;border:1px solid #2a3140;border-radius:10px;">
  <p style="margin:0 0 12px;font-size:15px;line-height:1.7;color:#ffffff;font-weight:800;">{{label1}}<br><span style="font-size:13px;line-height:1.65;color:#38bdf8;font-weight:400;word-break:break-all;">{{url1}}</span></p>
  <p style="margin:0;font-size:15px;line-height:1.7;color:#ffffff;font-weight:800;">{{label2}}<br><span style="font-size:13px;line-height:1.65;color:#38bdf8;font-weight:400;word-break:break-all;">{{url2}}</span></p>
</section>
```
