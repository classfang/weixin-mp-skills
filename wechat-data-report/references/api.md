# 微信公众号数据统计 API

这些说明是官方微信文档的精简索引。当字段、权限或错误码变化时，应核对官方文档。

## 官方文档

- 数据统计接口介绍：https://developers.weixin.qq.com/doc/subscription/guide/product/analysis_data/analysis_data.html
- 用户增减数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/user/api_getusersummary.html
- 累计用户数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/user/api_getusercumulate.html
- 获取发表内容每日阅读数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getarticleread.html
- 获取发表内容每日分享数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getarticleshare.html
- 获取发表内容概况总数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getbizsummary.html
- 获取发表内容发表详细数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getarticletotaldetail.html
- 获取图文阅读概况数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getuserread.html
- 获取图文转发概况数据：https://developers.weixin.qq.com/doc/subscription/api/wedata/news/api_getusershare.html
- 消息分析数据：https://developers.weixin.qq.com/doc/subscription/guide/product/analysis_data/analysis_data.html
- 接口分析数据：https://developers.weixin.qq.com/doc/subscription/guide/product/analysis_data/analysis_data.html

服务号路径通常将 `/doc/subscription/` 替换为 `/doc/service/`；调用域名和接口路径保持 `https://api.weixin.qq.com`。

## 通用请求

数据接口均为服务端调用：

```text
POST https://api.weixin.qq.com/datacube/API_NAME?access_token=ACCESS_TOKEN
```

请求体：

```json
{
  "begin_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

## 重要限制

- 官方建议每天上午 8 点后查询前一天数据。
- `end_date` 通常最大为昨天。
- 用户增减数据 `getusersummary` 明确最大跨度 7 天。
- 图文和发表内容类接口建议按日请求；脚本默认按日分片以避免 `61500/61501`。
- 数据库只保存 2014-12-01 之后的数据。
- 图文阅读量过低时可能不会返回统计结果。
- 建议本地保存已拉取数据，减少重复调用。

## 脚本内置数据集

- `user-summary`：`/datacube/getusersummary`，用户增减数据。
- `user-cumulate`：`/datacube/getusercumulate`，累计用户数据。
- `article-summary-legacy`：`/datacube/getarticlesummary`，旧图文群发每日数据；官方提示停止维护，优先使用新接口。
- `article-total-legacy`：`/datacube/getarticletotal`，旧图文群发总数据。
- `article-read`：`/datacube/getuserread`，图文阅读概况。
- `article-read-hour`：`/datacube/getuserreadhour`，图文阅读分时。
- `article-share`：`/datacube/getusershare`，图文转发概况。
- `article-share-hour`：`/datacube/getusersharehour`，图文转发分时。
- `article-daily-read`：`/datacube/getarticleread`，发表内容每日阅读。
- `article-daily-share`：`/datacube/getarticleshare`，发表内容每日分享。
- `biz-summary`：`/datacube/getbizsummary`，发表内容概况总数据。
- `article-total-detail`：`/datacube/getarticletotaldetail`，发表内容详细数据。
- `message-summary`：`/datacube/getupstreammsg`，消息发送概况。
- `message-hour`：`/datacube/getupstreammsghour`，消息发送分时。
- `message-week`：`/datacube/getupstreammsgweek`，消息发送周数据。
- `message-month`：`/datacube/getupstreammsgmonth`，消息发送月数据。
- `message-dist`：`/datacube/getupstreammsgdist`，消息发送分布。
- `message-dist-week`：`/datacube/getupstreammsgdistweek`，消息发送分布周数据。
- `message-dist-month`：`/datacube/getupstreammsgdistmonth`，消息发送分布月数据。
- `interface-summary`：`/datacube/getinterfacesummary`，被动回复概要。
- `interface-hour`：`/datacube/getinterfacesummaryhour`，被动回复分时。

## 常见字段

用户数据：

- `ref_date`：统计日期。
- `user_source`：用户来源渠道。
- `new_user`：新增关注。
- `cancel_user`：取消关注。
- `cumulate_user`：累计用户。

文章数据：

- `title`：文章标题。
- `msgid`：通常由 `msg_data_id` 与 `index` 组成。
- `int_page_read_user` / `int_page_read_count`：图文页阅读人数/次数。
- `share_user` / `share_count`：分享人数/次数。
- `add_to_fav_user` / `add_to_fav_count`：收藏人数/次数。
- `ori_page_read_user` / `ori_page_read_count`：原文页阅读人数/次数。

## 常见错误

- `40001`：access token 无效、过期、AppSecret 错误或 token 属于错误账号。
- `40164`：调用 IP 未配置到白名单。
- `48001`：接口权限不足。
- `61500`：日期格式或范围错误。
- `61501`：日期跨度超过接口限制。
- `61503`：指定日期数据尚未生成，稍后重试。

## 解读建议

- 不把空列表直接解释为表现为 0；先判断权限、日期和数据是否已生成。
- 阅读、分享、收藏需要结合文章标题、发布时间、推送位置和封面一起看。
- 小样本内容要避免过度解释百分比。
- 对比多篇文章时，优先使用同一时间窗、同一账号、相近推送方式的数据。
