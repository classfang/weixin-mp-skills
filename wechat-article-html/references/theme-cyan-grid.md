# 主题：青格笔记

适用于备考计划、学习复盘、资料清单、知识整理和教程笔记类文章。该主题抽取自掘金文章《软考高级〈系统架构设计师〉倒计时40天 复习计划》的排版风格：浅青网格纸背景、青色章节标题、紧凑正文、淡青引用块和清爽表格。

## 设计令牌

- 页面背景：`#f5fbff`
- 容器背景：`#ffffff`
- 正文文字：`#2b2b2b`
- 弱化文字：`#595959`
- 标题：`#4dd0e1`
- 主强调色：`#4dd0e1`
- 次强调色：`#26c6da`
- 网格线：`rgba(159,219,252,0.15)`
- 柔和表面：`rgba(77,208,225,0.08)`
- 引用表面：`rgba(77,208,225,0.15)`
- 代码背景：`#f8f8f8`
- 表头背景：`#f6f6f6`
- 边框：`#e6f5fa`
- 字体栈：`-apple-system,system-ui,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif`
- 等宽字体栈：`Menlo,Monaco,Consolas,'Courier New',monospace`

## 页面外壳

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
</head>
<body style="margin:0;padding:0;background:#f5fbff;color:#2b2b2b;font-family:-apple-system,system-ui,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;line-height:1.75;">
  <section style="box-sizing:border-box;max-width:680px;margin:0 auto;padding:26px 18px 52px;background-color:#ffffff;background-image:linear-gradient(90deg,rgba(159,219,252,0.15) 3%,transparent 0),linear-gradient(180deg,rgba(159,219,252,0.15) 3%,transparent 0);background-size:20px 20px;background-position:50%;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 auto 28px;border-radius:6px;box-shadow:0 0 16px rgba(110,110,110,0.35);">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:20px auto 10px;border-radius:6px;box-shadow:0 0 16px rgba(110,110,110,0.35);">
```

### 图片说明

```html
<p style="margin:0 0 22px;font-size:13px;line-height:1.6;color:#595959;text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="box-sizing:border-box;margin:0 auto 22px;padding:22px 0 14px;max-width:100%;font-size:28px;line-height:1.45;font-weight:800;color:#4dd0e1;text-align:center;letter-spacing:0;word-break:break-word;border-bottom:3px solid rgba(77,208,225,0.8);">{{title}}</h1>
<p style="margin:0 0 24px;font-size:15px;line-height:1.9;color:#595959;letter-spacing:1px;word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:34px 0 20px;padding:0 0 10px;border-bottom:4px solid #4dd0e1;">
  <h2 style="margin:0;font-size:24px;line-height:1.45;font-weight:800;color:#4dd0e1;letter-spacing:0;">{{heading}}</h2>
</section>
```

### 小节标题

```html
<section style="margin:28px 0 14px;padding:0 0 8px;border-bottom:2px solid #4dd0e1;">
  <h3 style="margin:0;font-size:18px;line-height:1.55;font-weight:800;color:#2b2b2b;letter-spacing:0;">{{heading}}</h3>
</section>
```

### 段落

```html
<p style="margin:0 0 18px;font-size:15px;line-height:1.85;color:#2b2b2b;letter-spacing:1px;word-spacing:1px;">{{text}}</p>
```

### 强调短语

```html
<strong style="color:#26c6da;font-weight:800;">{{text}}</strong>
```

### 行内代码

```html
<span style="display:inline-block;margin:0 2px;padding:1px 6px;border-radius:3px;background:rgba(77,208,225,0.08);color:#26c6da;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:0.92em;">{{code}}</span>
```

### 引用块

```html
<section style="position:relative;margin:24px 0;padding:20px 22px;border-left:4px solid #26c6da;background:rgba(77,208,225,0.15);border-radius:4px;">
  <p style="margin:0;font-size:15px;line-height:2;color:#595959;letter-spacing:1px;">{{quote}}</p>
</section>
```

### 多项列表

```html
<section style="margin:14px 0 22px;padding:14px 16px 14px 24px;background:rgba(77,208,225,0.05);border:1px solid #e6f5fa;border-radius:6px;">
  <p style="margin:0 0 10px;font-size:15px;line-height:1.85;color:#595959;">{{item1}}</p>
  <p style="margin:0 0 10px;font-size:15px;line-height:1.85;color:#595959;">{{item2}}</p>
  <p style="margin:0;font-size:15px;line-height:1.85;color:#595959;">{{item3}}</p>
</section>
```

### 复盘卡片

```html
<section style="margin:18px 0 24px;padding:16px 18px;background:#ffffff;border:1px solid #e6f5fa;border-radius:6px;box-shadow:0 0 10px rgba(77,208,225,0.10);">
  <p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:#26c6da;font-weight:800;">{{title}}</p>
  <p style="margin:0;font-size:15px;line-height:1.85;color:#2b2b2b;">{{text}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:15px 12px;background:#f8f8f8;color:#333333;border-radius:4px;box-shadow:0 0 8px rgba(110,110,110,0.35);word-break:break-all;overflow-wrap:anywhere;font-size:12px;line-height:1.75;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 表格

```html
<section style="margin:18px 0 24px;overflow-x:auto;border:1px solid #f6f6f6;border-radius:4px;background:#ffffff;">
  <table style="width:100%;border-collapse:collapse;font-size:12px;line-height:1.8;color:#2b2b2b;">
    <thead style="background:#f6f6f6;color:#000000;text-align:left;">
      <tr>
        <th style="padding:12px 7px;border:1px solid #f6f6f6;">{{head1}}</th>
        <th style="padding:12px 7px;border:1px solid #f6f6f6;">{{head2}}</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background:rgba(77,208,225,0.05);">
        <td style="padding:12px 7px;border:1px solid #f6f6f6;">{{cell1}}</td>
        <td style="padding:12px 7px;border:1px solid #f6f6f6;">{{cell2}}</td>
      </tr>
    </tbody>
  </table>
</section>
```

### 分隔线

```html
<section style="margin:32px 0;border-top:1px solid #4dd0e1;font-size:0;line-height:0;">&nbsp;</section>
```

### 参考文章

```html
<section style="margin:18px 0 24px;padding:14px 16px;background:rgba(77,208,225,0.05);border:1px solid #e6f5fa;border-radius:6px;">
  <p style="margin:0 0 6px;font-size:13px;color:#26c6da;font-weight:800;">参考文章</p>
  <p style="margin:0 0 8px;font-size:15px;line-height:1.7;color:#2b2b2b;font-weight:700;">{{label}}</p>
  <p style="margin:0;font-size:13px;line-height:1.65;color:#595959;word-break:break-all;">{{url}}</p>
</section>
```
