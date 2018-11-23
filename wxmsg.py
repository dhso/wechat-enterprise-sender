# -*- coding: utf-8 -*-
# /usr/bin/python

# 使用方法 python ./wxmsg.py "corpid" "corpsecret" "agentid"

import sys
import requests
import json
from bottle import request, run, post, install
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='wxmsg.db'))


@post('/wechat/corp/send')
def wechat_corp_send(db):
    try:
        corpid = request.json.get('corpid', sys.argv[1])
        corpsecret = request.json.get('corpsecret', sys.argv[2])
        message_data = parseMessageData(request)
        access_token = getAccessToken(db, corpid, corpsecret)
        return sendWechatMessage(db, access_token, message_data)
    except Exception, e:
        return {
            "errcode": -1,
            "errmsg": e.message
        }


def parseMessageData(request):
    message_data = {}
    message_data["touser"] = '|'.join(request.json['users'])
    message_data["agentid"] = request.json.get('agentid', sys.argv[3])
    message_data["safe"] = request.json.get('safe', 0)
    message_data["msgtype"] = request.json.get('msgtype', 'text')
    if message_data["msgtype"] == 'text':
        message_data[message_data["msgtype"]] = {
            "content": request.json.get('msgdata', u'空消息')}
    elif message_data["msgtype"] == 'textcard':
        message_data[message_data["msgtype"]] = request.json.get('msgdata', {})
    else:
        raise Exception("Invalid Msgtype!")
    return message_data


def getAccessToken(db, corpid, corpsecret):
    if not corpid or not corpsecret:
        raise Exception("Invalid corpid or corpsecret!")
    row = db.execute(
        "SELECT * FROM access_tokens WHERE corpid = ? and expires_date > datetime('now','localtime')", [corpid]).fetchone()
    if row:
        return row['access_token']
    token_data = requestAccessToken(corpid, corpsecret)
    access_token = token_data['access_token']
    sql = "REPLACE INTO access_tokens VALUES (?, ?, datetime('now', 'localtime', '+{} seconds'))".format(
        token_data['expires_in'])
    db.execute(sql, [corpid, access_token])
    return token_data['access_token']


def requestAccessToken(corpid, corpsecret):
    access_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
        corpid, corpsecret)
    access_token_response = requests.get(access_token_url)
    return json.loads(access_token_response.content)


def sendWechatMessage(db, access_token, message_data):
    send_message_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(
        access_token)
    json_headers = {'Content-Type': 'application/json'}
    result = requests.post(url=send_message_url,
                           headers=json_headers, data=json.dumps(message_data))
    db.execute("INSERT INTO message_send_logs VALUES (?, ?, datetime('now', 'localtime'))", [
               json.dumps(message_data), result.content])
    return json.loads(result.content)


run(host='0.0.0.0', port=8080, reloader=True, debug=False)
