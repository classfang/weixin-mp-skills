# 主题：蓝灰简报

视觉定位：蓝灰页面、严谨边框、大号关键数字和分隔条目。强调紧凑、冷静、摘要感和快速扫描，不绑定任何文章题材。

## 设计令牌

- 页面背景：`#eef2f6`
- 容器背景：`#ffffff`
- 正文文字：`#243141`
- 弱化文字：`#5f6f82`
- 标题：`#101828`
- 主强调色：`#1769aa`
- 次强调色：`#f59e0b`
- 柔和表面：`#f5f8fb`
- 数据表面：`#eaf3ff`
- 深色表面：`#132033`
- 边框：`#d8e1ea`
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
<body style="margin:0;padding:0;background:#eef2f6;color:#243141;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.84;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:24px 16px 52px;background:#ffffff;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 0 26px;border-radius:6px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:10px 0 10px;border-radius:6px;">
```

### 图片说明

```html
<p style="margin:0 0 22px;font-size:13px;line-height:1.65;color:#5f6f82;text-align:center;">{{caption}}</p>
```

### 页眉标签

```html
<section style="margin:0 0 16px;padding:10px 12px;background:#132033;border-radius:6px;">
  <p style="margin:0;font-size:12px;line-height:1.5;color:#ffffff;font-weight:800;">{{report_type}}</p>
  <p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:#b9c7d8;">{{period}}</p>
</section>
```

### 标题和导语

```html
<section style="margin:0 0 26px;padding:0 0 18px;border-bottom:2px solid #101828;">
  <h1 style="margin:0 0 12px;font-size:27px;line-height:1.35;font-weight:900;color:#101828;letter-spacing:0;word-break:break-word;">{{title}}</h1>
  <p style="margin:0;font-size:16px;line-height:1.78;color:#5f6f82;word-break:break-word;">{{deck}}</p>
</section>
```

### 关键数字

```html
<section style="margin:20px 0 28px;padding:18px;background:#eaf3ff;border:1px solid #b8d8f5;border-radius:6px;">
  <p style="margin:0 0 6px;font-size:13px;color:#1769aa;font-weight:800;">{{label}}</p>
  <p style="margin:0 0 6px;font-size:32px;line-height:1.15;color:#101828;font-weight:900;">{{metric}}</p>
  <p style="margin:0;font-size:14px;line-height:1.65;color:#405166;">{{explain}}</p>
</section>
```

### 章节标题

```html
<section style="margin:36px 0 18px;padding:0 0 10px;border-bottom:1px solid #d8e1ea;">
  <p style="margin:0 0 6px;font-size:13px;color:#1769aa;font-weight:900;">{{number}}</p>
  <h2 style="margin:0;font-size:22px;line-height:1.42;font-weight:900;color:#101828;">{{heading}}</h2>
</section>
```

### 段落

```html
<p style="margin:0 0 16px;font-size:16px;line-height:1.84;color:#243141;">{{text}}</p>
```

### 高亮信息

```html
<section style="margin:22px 0 28px;padding:16px 16px;background:#f5f8fb;border-left:4px solid #1769aa;border-top:1px solid #d8e1ea;border-right:1px solid #d8e1ea;border-bottom:1px solid #d8e1ea;border-radius:6px;">
  <p style="margin:0 0 8px;font-size:15px;color:#101828;font-weight:800;">{{title}}</p>
  <p style="margin:0;font-size:15px;line-height:1.78;color:#405166;">{{text}}</p>
</section>
```

### 对比条目

```html
<section style="margin:18px 0 24px;padding:0;border:1px solid #d8e1ea;border-radius:6px;overflow:hidden;">
  <p style="margin:0;padding:12px 14px;background:#f5f8fb;font-size:15px;line-height:1.7;color:#243141;">{{item1}}</p>
  <p style="margin:0;padding:12px 14px;border-top:1px solid #d8e1ea;font-size:15px;line-height:1.7;color:#243141;">{{item2}}</p>
  <p style="margin:0;padding:12px 14px;border-top:1px solid #d8e1ea;font-size:15px;line-height:1.7;color:#243141;">{{item3}}</p>
</section>
```

### 醒目提示

```html
<section style="margin:24px 0 30px;padding:16px 18px;background:#fffbeb;border:1px solid #f6d58a;border-radius:6px;">
  <p style="margin:0 0 8px;font-size:15px;color:#92400e;font-weight:800;">{{label}}</p>
  <p style="margin:0;font-size:15px;line-height:1.78;color:#704214;">{{text}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:16px;background:#132033;color:#dbeafe;border-radius:6px;word-break:break-all;overflow-wrap:anywhere;font-size:14px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 参考资料组

搭配文末唯一的“参考资料”章节标题使用。多个来源连续列出，不要为每条资料重复写“参考资料”或“参考文章”标签。按来源数量复制或删除条目段落，最后一条使用 `margin:0`。

```html
<section style="margin:18px 0 24px;padding:15px 16px;background:#f5f8fb;border:1px solid #d8e1ea;border-radius:6px;">
  <p style="margin:0 0 12px;font-size:15px;line-height:1.7;color:#101828;font-weight:800;">{{label1}}<br><span style="font-size:13px;line-height:1.65;color:#1769aa;font-weight:400;word-break:break-all;">{{url1}}</span></p>
  <p style="margin:0;font-size:15px;line-height:1.7;color:#101828;font-weight:800;">{{label2}}<br><span style="font-size:13px;line-height:1.65;color:#1769aa;font-weight:400;word-break:break-all;">{{url2}}</span></p>
</section>
```
