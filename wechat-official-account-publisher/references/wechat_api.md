# 微信公众号 API 说明

这些说明是官方微信文档的精简索引。当接口行为变化，或遇到不熟悉的错误码时，应核对官方文档。

## 官方文档

- 微信开发者平台入口：https://developers.weixin.qq.com/platform
- 获取 access token：https://developers.weixin.qq.com/doc/service/api/base/api_getaccesstoken.html
- 上传文章内容中的图片：https://developers.weixin.qq.com/doc/service/api/notify/message/api_uploadimage.html
- 草稿管理概览：https://developers.weixin.qq.com/doc/service/guide/product/draft.html
- 新建草稿：https://developers.weixin.qq.com/doc/service/api/draftbox/draftmanage/api_draft_add
- 发布能力概览：https://developers.weixin.qq.com/doc/service/guide/product/publish.html
- 提交草稿发布：https://developers.weixin.qq.com/doc/service/api/public/api_freepublish_submit
- 查询发布状态：https://developers.weixin.qq.com/doc/service/api/public/api_freepublish_get

## 核心流程

1. 使用 AppID/AppSecret 获取 `access_token`，或使用有效的 `WECHAT_ACCESS_TOKEN`。
2. 使用 `/cgi-bin/media/uploadimg` 上传本地文内图片，并将本地 `src` 值替换为微信返回的 URL。
3. 使用 `/cgi-bin/material/add_material?type=image` 将封面图上传为永久图片素材，获得 `thumb_media_id`；也可以直接使用用户提供的 `thumb_media_id`。
4. 使用 `/cgi-bin/draft/add` 创建草稿。
5. 只有在用户明确确认后，才使用返回的草稿 `media_id` 调用 `/cgi-bin/freepublish/submit` 提交发布。
6. 使用 `publish_id` 轮询 `/cgi-bin/freepublish/get`，直到微信返回成功或终止性失败状态。

## 草稿文章结构

`articles[0]` 的常见字段：

```json
{
  "article_type": "news",
  "title": "文章标题",
  "author": "作者",
  "digest": "摘要",
  "content": "<section>HTML 正文</section>",
  "content_source_url": "https://example.com/source",
  "thumb_media_id": "MEDIA_ID",
  "need_open_comment": 0,
  "only_fans_can_comment": 0
}
```

需要时可加入可选封面裁剪字段：

- `pic_crop_235_1`：`x1_y1_x2_y2`
- `pic_crop_1_1`：`x1_y1_x2_y2`

## 常见错误

- `40001`：access token 无效或过期，AppSecret 错误，或 token 属于错误账号。
- `40164`：调用方 IP 不在公众号 API 白名单中。
- `48001`：账号未获得该 API 权限。
- `40005`：上传图片文件类型无效。
- `40009`：图片体积过大。
- `53503`：草稿未通过发布检查。
- `53504` 或 `53505`：微信要求在公众平台后台手动处理。

## 权限说明

微信按账号类型说明发布权限。根据已检查的文档，发布相关接口适用于服务号和已认证公众号；部分个人、未认证或不支持的账号可能无法调用。如果出现配置缺失、IP 白名单、接口权限或发布权限错误，提示用户打开 `https://developers.weixin.qq.com/platform` 获取 AppID/AppSecret、配置服务器 IP 白名单，并检查公众号认证状态和接口权限，再重试。
