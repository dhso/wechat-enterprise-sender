#-*- coding: utf-8 -*-
#/usr/bin/python

#使用方法 python ./wxmsg.py "corpid" "corpsecret" "agentid"

import sys
import requests
import json
from bottle import request, run, post, install
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='wxmsg.db'))

@post('/wechat/message/send')
def wechat_message_send(db):
    users = request.json['users']
    message = request.json['message']
    corpid = request.json.get('corpid', sys.argv[1])
    corpsecret = request.json.get('corpsecret', sys.argv[2])
    agentid = request.json.get('agentid', sys.argv[3])
    access_token = getAccessToken(db, corpid, corpsecret)
    message_data = { 
            "touser": '|'.join(users),
            "msgtype": "text", 
            "agentid": agentid,
            "text":{ "content": message },
            "safe": 0 }
    sendWechatMessage(db, access_token, message_data)
    return {'result':'success'}

@post('/wechat/card/send')
def wechat_card_send(db):
    users = request.json['users']
    title = request.json.get('title', u'通知')
    message = request.json.get('message', u'空消息')
    url = request.json.get('url', u'_blank')
    btntxt = request.json.get('btntxt', u'查看')
    corpid = request.json.get('corpid', sys.argv[1])
    corpsecret = request.json.get('corpsecret', sys.argv[2])
    agentid = request.json.get('agentid', sys.argv[3])
    access_token = getAccessToken(db, corpid, corpsecret)
    message_data = { 
            "touser": '|'.join(users),
            "msgtype": "textcard", 
            "agentid": agentid,
            "textcard":{ "title": title,
                "description":message,
                "url":url,
                "btntxt":btntxt },
            "safe": 0 }
    sendWechatMessage(db, access_token, message_data)
    return {'result':'success'}

def getAccessToken(db, corpid, corpsecret):
    row = db.execute("SELECT * FROM access_tokens WHERE corpid = ? and expires_date > datetime('now','localtime')", [corpid] ).fetchone()
    if row:
        return row['access_token']
    token_data = requestAccessToken(corpid, corpsecret)
    access_token = token_data['access_token']
    sql = "REPLACE INTO access_tokens VALUES (?, ?, datetime('now', 'localtime', '+{} seconds'))".format(token_data['expires_in'])
    db.execute(sql, [corpid, access_token])
    return token_data['access_token']

def requestAccessToken(corpid, corpsecret):
    access_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(corpid, corpsecret)
    access_token_response = requests.get(access_token_url)
    return json.loads(access_token_response.content)

def sendWechatMessage(db, access_token, message_data):
    send_message_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token)
    json_headers = {'Content-Type': 'application/json'}
    result = requests.post(url=send_message_url, headers=json_headers, data=json.dumps(message_data))
    db.execute("INSERT INTO message_send_logs VALUES (?, ?, datetime('now', 'localtime'))", [json.dumps(message_data), result.content])
    return json.loads(result.content)

run(host='0.0.0.0', port=8080, reloader=True, debug=False)