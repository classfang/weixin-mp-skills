# 主题：灵动蓝

视觉定位：灵动蓝色、轻快段落和清楚标题。主题由 markdown2wechat 的 `灵动蓝.json` 转换而来，已加 `m2w-` 参数前缀以避免和现有主题冲突。

## 设计令牌

- 页面背景：`rgba(0, 0, 0, 0)`
- 容器背景：`rgba(0, 0, 0, 0)`
- 正文文字：`rgba(51, 51, 51, 1)`
- 弱化文字：`rgba(51, 51, 51, 1)`
- 标题：`rgba(51, 51, 51, 1)`
- 主强调色：`rgba(255, 255, 255, 1)`
- 柔和表面：`rgba(255, 249, 249, 1)`
- 边框：`rgba(178, 174, 197, 1)`
- 源样式哈希：`fb529411fff3`
- 字体栈：`Optima,Microsoft YaHei,PingFangSC-regular,serif`
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
<body style="margin:0;padding:0;background:rgba(0, 0, 0, 0);color:rgba(51, 51, 51, 1);font-family:Optima,Microsoft YaHei,PingFangSC-regular,serif;line-height:1.8em;">
  <section style="margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;padding-top:0px;padding-bottom:0px;padding-left:10px;padding-right:10px;background-attachment:scroll;background-clip:border-box;background-color:rgba(0, 0, 0, 0);background-image:none;background-origin:padding-box;background-position-x:left;background-position-y:top;background-repeat:no-repeat;background-size:auto;width:auto;height:auto;font-family:Optima,Microsoft YaHei,PingFangSC-regular,serif;margin:0 auto;padding:26px 16px 52px;box-sizing:border-box;max-width:680px;color:rgba(51, 51, 51, 1);line-height:1.8em;">
    {{content}}
  </section>
</body>
</html>
```

## 组件

### 封面图

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:0 auto 28px;border-radius:6px;">
```

### 文内图片

```html
<img src="{{image_src}}" alt="{{alt}}" style="display:block;width:100%;max-width:100%;height:auto;margin:12px auto 10px;border-radius:6px;">
```

### 图片说明

```html
<p style="margin:0 0 22px;font-size:13px;line-height:1.7;color:rgba(51, 51, 51, 1);text-align:center;">{{caption}}</p>
```

### 标题和导语

```html
<h1 style="margin-top:30px;margin-bottom:15px;margin-left:0px;margin-right:0px;padding-top:0px;padding-bottom:0px;padding-left:0px;padding-right:0px;margin:0 0 18px;font-size:26px;line-height:1.42;font-weight:800;color:rgba(51, 51, 51, 1);letter-spacing:0;word-break:break-word;">{{title}}</h1>
<p style="margin:0 0 24px;font-size:15px;line-height:1.85;color:rgba(51, 51, 51, 1);word-break:break-word;">{{deck}}</p>
```

### 章节标题

```html
<section style="margin:34px 0 18px;">
  <h2 style="margin-top:30px;margin-bottom:15px;margin-left:0px;margin-right:0px;margin:0;font-size:22px;line-height:1.45;font-weight:800;color:rgba(51, 51, 51, 1);letter-spacing:0;">{{heading}}</h2>
</section>
```

### 小节标题

```html
<section style="margin:26px 0 14px;">
  <h3 style="margin-top:30px;margin-bottom:15px;margin-left:0px;margin-right:0px;padding-top:0px;padding-bottom:0px;padding-left:0px;padding-right:0px;margin:0;font-size:18px;line-height:1.55;font-weight:800;color:rgba(51, 51, 51, 1);letter-spacing:0;">{{heading}}</h3>
</section>
```

### 段落

```html
<p style="color:rgba(51, 51, 51, 1);font-size:16px;line-height:1.8em;letter-spacing:0em;text-align:left;text-indent:0em;margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;padding-top:8px;padding-bottom:8px;padding-left:0px;padding-right:0px;margin:0 0 16px;word-break:break-word;">{{text}}</p>
```

### 强调短语

```html
<strong style="color:rgba(255, 255, 255, 1);font-weight:normal;background-attachment:scroll;background-clip:border-box;background-color:rgba(0, 0, 0, 0);background-image:linear-gradient(90deg,rgba(50, 153, 210, 0.7) 0%,rgba(239, 189, 181, 0.7) 97.3%) , none;background-origin:padding-box;background-position-x:left;background-position-y:top;background-repeat:no-repeat;background-size:auto;width:auto;height:auto;margin-top:0px;margin-bottom:0px;margin-left:2px;margin-right:2px;padding-top:4px;padding-bottom:4px;padding-left:4px;padding-right:4px;border-top-style:none;border-bottom-style:none;border-left-style:none;border-right-style:none;border-top-width:3px;border-bottom-width:3px;border-left-width:3px;border-right-width:3px;border-top-color:rgba(0, 0, 0, 0.4);border-bottom-color:rgba(0, 0, 0, 0.4);border-left-color:rgba(0, 0, 0, 0.4);border-right-color:rgba(0, 0, 0, 0.4);border-top-left-radius:4px;border-top-right-radius:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;">{{text}}</strong>
```

### 引用块

```html
<section style="margin-top:20px;margin-bottom:20px;margin-left:0px;margin-right:0px;padding-top:10px;padding-bottom:10px;padding-left:20px;padding-right:10px;border-top-style:none;border-bottom-style:none;border-left-style:solid;border-right-style:none;border-top-width:3px;border-bottom-width:3px;border-left-width:3px;border-right-width:3px;border-top-color:rgba(0, 0, 0, 0.4);border-bottom-color:rgba(0, 0, 0, 0.4);border-left-color:rgba(178, 174, 197, 1);border-right-color:rgba(0, 0, 0, 0.4);border-top-left-radius:0px;border-top-right-radius:0px;border-bottom-right-radius:0px;border-bottom-left-radius:0px;background-attachment:scroll;background-clip:border-box;background-color:rgba(255, 249, 249, 1);background-image:none;background-origin:padding-box;background-position-x:left;background-position-y:top;background-repeat:no-repeat;background-size:auto;width:auto;height:auto;box-shadow:0px 0px 0px 0px rgba(0, 0, 0, 0);margin:22px 0;border-radius:0px;">
  <p style="color:rgba(102, 102, 102, 1);font-size:16px;line-height:1.8em;letter-spacing:0em;text-align:left;font-weight:normal;margin:0;word-break:break-word;">{{quote}}</p>
</section>
```

### 多项列表

```html
<section style="list-style-type:circle;margin-top:8px;margin-bottom:8px;margin-left:0px;margin-right:0px;padding-top:0px;padding-bottom:0px;padding-left:25px;padding-right:0px;margin:16px 0 24px;padding:14px 18px 14px 28px;background-color:rgba(255, 249, 249, 1);border:1px solid rgba(178, 174, 197, 1);border-radius:6px;">
  <p style="color:rgba(51, 51, 51, 1);font-size:16px;line-height:1.8em;letter-spacing:0em;text-align:left;text-indent:0em;margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;padding-top:8px;padding-bottom:8px;padding-left:0px;padding-right:0px;margin:0 0 10px;">{{item1}}</p>
  <p style="color:rgba(51, 51, 51, 1);font-size:16px;line-height:1.8em;letter-spacing:0em;text-align:left;text-indent:0em;margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;padding-top:8px;padding-bottom:8px;padding-left:0px;padding-right:0px;margin:0 0 10px;">{{item2}}</p>
  <p style="color:rgba(51, 51, 51, 1);font-size:16px;line-height:1.8em;letter-spacing:0em;text-align:left;text-indent:0em;margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;padding-top:8px;padding-bottom:8px;padding-left:0px;padding-right:0px;margin:0;">{{item3}}</p>
</section>
```

### 代码块

```html
<p style="display:block;box-sizing:border-box;max-width:100%;margin:16px 0 22px;padding:15px 14px;background-color:#1f2937;color:#f8fafc;border-radius:6px;word-break:break-all;overflow-wrap:anywhere;font-size:13px;line-height:1.75;font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;">{{escaped_code_with_br_and_nbsp}}</p>
```

### 表格

```html
<section style="margin:18px 0 24px;overflow-x:auto;border:1px solid rgba(178, 174, 197, 1);border-radius:6px;background:rgba(0, 0, 0, 0);">
  <table style="width:100%;border-collapse:collapse;font-size:13px;line-height:1.75;color:rgba(51, 51, 51, 1);">
    <thead>
      <tr>
        <th style="padding:10px 8px;border:1px solid rgba(178, 174, 197, 1);text-align:left;">{{head1}}</th>
        <th style="padding:10px 8px;border:1px solid rgba(178, 174, 197, 1);text-align:left;">{{head2}}</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:10px 8px;border:1px solid rgba(178, 174, 197, 1);">{{cell1}}</td>
        <td style="padding:10px 8px;border:1px solid rgba(178, 174, 197, 1);">{{cell2}}</td>
      </tr>
    </tbody>
  </table>
</section>
```

### 分隔线

```html
<section style="margin:32px 0;border-top:1px solid rgba(178, 174, 197, 1);font-size:0;line-height:0;">&nbsp;</section>
```

### 参考资料组

搭配文末唯一的“参考资料”章节标题使用。多个来源连续列出，不要为每条资料重复写“参考资料”或“参考文章”标签。按来源数量复制或删除条目段落，最后一条使用 `margin:0`。

```html
<section style="margin:18px 0 24px;padding:14px 16px;background:rgba(255, 249, 249, 1);border:1px solid rgba(178, 174, 197, 1);border-radius:6px;">
  <p style="margin:0 0 12px;font-size:15px;line-height:1.7;color:rgba(51, 51, 51, 1);font-weight:700;">{{label1}}<br><span style="font-size:13px;line-height:1.65;color:rgba(51, 51, 51, 1);font-weight:400;word-break:break-all;">{{url1}}</span></p>
  <p style="margin:0;font-size:15px;line-height:1.7;color:rgba(51, 51, 51, 1);font-weight:700;">{{label2}}<br><span style="font-size:13px;line-height:1.65;color:rgba(51, 51, 51, 1);font-weight:400;word-break:break-all;">{{url2}}</span></p>
</section>
```
