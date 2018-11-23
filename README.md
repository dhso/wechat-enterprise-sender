# wechat-enterprise-sender

微信企业版发送服务

## run

```
docker run -dt \
--name wechat-corp-sender \
-p 8080:8080 \
-e CORPID='YOUR CORPID' \
-e CORPSECRET="YOUR CORPSECRET" \
-e AGENTID="YOUR AGENTID" \
dhso/wechat-corp-sender
```

## api

- 文本消息

```
<domain>/wechat/corp/send

{
    "users":["u1","u2"],
	"agentid":"1000000", //可选
    "msgtype":"text",
    "msgdata":"这是一条消息"
}
```
- 卡片消息

```
<domain>/wechat/corp/send

{
    "users":["u1","u2"],
	"agentid":"1000000", //可选
    "msgtype":"textcard",
    "msgdata":{
		"title" : "领奖通知",
		"description" : "<div class='gray'>2016年9月26日</div><div class='normal'>恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class='highlight'>请于2016年10月10日前联系行政同事领取</div>",
		"url" : "URL",
		"btntxt":"更多"
   }
}
```
