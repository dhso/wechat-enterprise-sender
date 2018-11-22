# wechat-enterprise-sender
微信企业版发送服务

## run

```
docker run -dt \
--name wechat-sender \
-p 8080:8080 \
-e CORPID='YOUR CORPID' \
-e CORPSECRET="YOUR CORPSECRET" \
-e AGENTID="YOUR AGENTID" \
dhso/wechat-sender
```
## api

- 普通消息

```
<domain>/wechat/message/send

{
	"users":["u1","u2"],
	"message":"这是一条消息"
}

```

- 卡片消息

```
<domain>/wechat/card/send

{
    "users":["u1","u2"],
    "title":"领奖信息",
    "message":"<div class='gray'>2016年9月26日</div><div class='normal'>恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class='highlight'>请于2016年10月10日前联系行政同事领取</div>",
	"url":"https://www.qq.com",
	"btntxt":"查看"
}
```
