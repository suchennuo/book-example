
import xmltodict
from openwx.messages.messages import MessageMetaClass, UnknownMessage
"""
<xml>
<ToUserName>< ![CDATA[toUser] ]></ToUserName>
<FromUserName>< ![CDATA[fromUser] ]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType>< ![CDATA[text] ]></MsgType>
<Content>< ![CDATA[你好] ]></Content>
</xml>
"""
def parse_xml(text):
    xml_dict = xmltodict.parse(text)["xml"]
    xml_dict["raw"] = text
    return xml_dict


def process_message(message):
    message["type"] = message.pop("MsgType").lower()
    if message["type"] == 'event':
        #TODO: 事件的处理，订阅，取消订阅等
        pass
    else:
        # Python 字典(Dictionary) get() 函数返回指定键的值，如果值不在字典中返回默认值。
        message_type = MessageMetaClass.TYPES.get(message["type"], UnknownMessage)
    return message_type(message)
