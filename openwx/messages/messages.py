
import six
from .base import RobotMetalClass
from .entries import StringEntry, IntEntry, FloatEntry

class MessageMetaClass(RobotMetalClass):
    pass

# 声明类 WeChatMessage 的 metaclass 是 类 MessageMetaClass
# MessageMetaClass 需要是一个 metaclass
# python3 中 class WeChatMessage(object, mateclass = MessageMetaClass)
# http://www.cnblogs.com/Security-Darren/p/4094959.html


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    message_id = IntEntry('MsgId', 0)
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime', 0)

    def __init__(self, message):
        # 对象的属性存储在对象的 __dict__ 属性中
        self.__dict__.update(message)

    # dict.update(dict2) 把 dict2 的键值对更新到 dict 里


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = StringEntry('Content')

class ImageMessage(WeChatMessage):
    __type__ = 'image'
    img = StringEntry('PicUrl')


class UnknownMessage(WeChatMessage):
    __type__ = 'unknown'
