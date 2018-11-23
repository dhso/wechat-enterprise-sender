docker service create \
--name wechat-corp-sender-qa \
--network lr_net \
-e CORPID='' \
-e CORPSECRET="" \
-e AGENTID="1000003" \
--publish 18080:8080 \
--constraint 'node.hostname == lr.nt.003' \
--replicas 1 \
dhso/wechat-corp-sender:latest

