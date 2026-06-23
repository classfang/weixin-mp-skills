# 微信公众号留言管理 API

这些说明是官方微信文档的精简索引。当接口行为变化、错误码不明确，或需要确认权限范围时，应核对官方文档。

## 官方文档

- 留言管理概览：https://developers.weixin.qq.com/doc/subscription/guide/product/comments.html
- 查看指定文章评论：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_listcomment.html
- 打开文章评论：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_openarticlecomment.html
- 关闭文章评论：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_closecomment.html
- 评论标记精选：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_electcomment.html
- 评论取消精选：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_unelectcomment.html
- 删除评论：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_delcomment.html
- 回复评论：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_replycomment.html
- 删除回复：https://developers.weixin.qq.com/doc/subscription/api/leaving/api_delreplycomment.html

服务号路径通常将 `/doc/subscription/` 替换为 `/doc/service/`；调用域名和接口路径保持 `https://api.weixin.qq.com`。

## 接口与参数

通用参数：

- `access_token`：接口调用凭证。
- `msg_data_id`：群发返回的 `msg_data_id`。
- `index`：多图文序号，从 0 开始；未传时默认第一篇。
- `user_comment_id`：评论 ID，针对单条留言操作时必填。

接口列表：

- `POST /cgi-bin/comment/list`：查看评论。
  - 请求体：`msg_data_id`、`index`、`begin`、`count`、`type`。
  - `count` 必须小于 50；脚本默认最大使用 49。
  - `type=0` 全部，`type=1` 普通评论，`type=2` 精选评论。
- `POST /cgi-bin/comment/open`：打开已群发文章评论。
- `POST /cgi-bin/comment/close`：关闭已群发文章评论。
- `POST /cgi-bin/comment/markelect`：标记精选。
- `POST /cgi-bin/comment/unmarkelect`：取消精选。
- `POST /cgi-bin/comment/delete`：删除评论。
- `POST /cgi-bin/comment/reply/add`：回复评论，额外传 `content`。
- `POST /cgi-bin/comment/reply/delete`：删除评论回复。

## 返回字段

`comment/list` 常见返回字段：

- `total`：评论总数。
- `comment[].user_comment_id`：评论 ID。
- `comment[].create_time`：评论时间戳。
- `comment[].content`：评论内容。
- `comment[].comment_type`：是否精选，0 为未精选，1 为精选。
- `comment[].openid`：用户 OpenID；非微信身份评论可能不返回。
- `comment[].reply.content`：已回复内容。
- `comment[].reply.create_time`：回复时间戳。

## 常见错误

- `40001`：access token 无效、过期、AppSecret 错误或 token 属于错误账号。
- `40164`：调用 IP 未配置到白名单。
- `45009`：超过接口每日调用额度。
- `48001`：接口权限不足。
- `88000`：账号没有留言权限。
- `88001`：图文不存在。
- `88005`：评论已经回复过。
- `88007`：回复内容为空或超过长度限制。
- `88008`：评论不存在。
- `88010`：`count <= 0` 或 `count > 50`。

## 操作边界

- 读取评论可以直接执行；其余写操作必须先 dry-run。
- 删除评论和删除回复不可轻易恢复，必须得到明确确认。
- 回复评论应先输出草稿，由用户确认后再执行。
- 精选评论会改变公开展示结果，应将理由和评论 ID 一并展示给用户。
