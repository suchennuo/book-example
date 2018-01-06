from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed

from django.views.decorators.csrf import csrf_exempt
import logging
# Create your views here.

from . import utils
from openwx.robot import WeChatRobot, BaseRobot

from django.utils.encoding import smart_str
import xml.etree.ElementTree as etree



logger = logging.getLogger(__name__)

# Django 开发 需要注意 csrf_token

# robot = WeChatRobot(token=utils.generate_token())
robot = WeChatRobot()

robot.config["APP_ID"] = "wx1a96816e77bd8971"  # "wxc05433d37133e7bb"
robot.config["APP_SECRET"] = "965ca48d1f4d9a1a7005230bd97c1ac0"  # "5bfa787f37541860d6f2c2f1d83b5ca2"
robot.config["TOKEN"] = "tokenhere"

# client = robot.client
#
# client.create_menu({
#     "button":[{
#         "type": "click",
#         "name": "取你🐶命",
#         "key": "funny"
#     }]
# })


# @robot.key_click("funny")
# def funny(message):
#     return "It's not funny."


@robot.handler
def hello(message, session):

    # json = client.get_user_info(user_id=message.source)
    # nickname = json['nickname']

    count = session.get("count", 0)+1
    session["count"] = count
    return "Hi, stranger. You have sent {} messages to me.".format( count)


@csrf_exempt
def access_token(request):
    print('access_token')
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    signature = request.GET.get("signature", "")

    print('signature ' + signature)

    print("request text " + request.body.decode('utf-8'))
    if not utils.check_signature(
        token="tokenhere",
        timestamp=timestamp,
        nonce=nonce,
        signature=signature,
    ):
        return HttpResponseForbidden()

    if request.method == "GET":
        return HttpResponse(request.GET.get("echostr", ""))
    elif request.method == "POST":
        #
        # othercontent = auto_reply(request)
        # print("Response " + othercontent)
        # return HttpResponse(othercontent)

        message = robot.parse_message(
            request.body,
            timestamp=timestamp,
            nonce=nonce,
            msg_signature=request.GET.get("msg_signature")
        )
        return HttpResponse(
            robot.get_encrypted_reply(message),
            content_type="application/xml;charset=utf-8"
        )

    return HttpResponseNotAllowed(['GET', 'POST'])







def auto_reply(request):
    try:
        webData = request.body
        xmlData = etree.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text
        toUser = FromUserName
        fromUser = ToUserName
        if msg_type == 'text':
            content = "Hello, stranger."
            replyMsg = TextMsg(toUser, fromUser, content)
            print("post success ")
            return replyMsg.send()
    except Exception:
        return Exception

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)



