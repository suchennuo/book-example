import six
from openwx.messages.entries import StringEntry, IntEntry, FloatEntry
from openwx.messages.base import RobotMetalClass

class EventMetalClass(RobotMetalClass):
    pass

@six.add_metaclass(EventMetalClass)
class WeChatEvent(object):
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime')
    message_id = IntEntry('MsgID', 0)

    def __init__(self, message):
        self.__dict__.update(message)

class SimpleEvent(WeChatEvent):
    key = StringEntry('EventKey')


class TicketEvent(WeChatEvent):
    key = StringEntry('EventKey')
    ticket = StringEntry('Ticket')

class ClickEvent(SimpleEvent):
    __type__ = 'click_event'

class UnknownEvent(WeChatEvent):
    __type__ = 'unknow_event'