docker service create \
--name wechat-corp-sender-qa \
--network lr_net \
-e CORPID='ww81062fdb63d4b5a2111' \
-e CORPSECRET="y6f4b7oETmOTJ7_DmyZsnAfZ-K9vqEOvIwOgZ86XPy0111" \
-e AGENTID="1000003" \
--publish 18080:8080 \
--constraint 'node.hostname == lr.nt.003' \
--replicas 1 \
dhso/wechat-corp-sender:latest

