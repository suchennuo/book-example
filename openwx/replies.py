
import time
from collections import namedtuple, defaultdict

from openwx.utils import to_text, is_string

TAG = "replies.py"


def renderable_named_tuple(typename, field_names, template):
    class TMP(namedtuple(typename=typename, field_names=field_names)):
        __TEMPLATE__ = template

        @property
        def args(self):
            return dict(zip(self._fields, self))

        def process_args(self, **kwargs):
            args = defaultdict(str)
            for k, v in kwargs.items():
                if is_string(v):
                    v = to_text(v)
                args[k] = v
            return args

        def render(self):
            return to_text(self.__TEMPLATE__.format(**self.process_args(self.args)))

    TMP.__name__ = typename
    return TMP


class WeChatReply(object):

    def process_args(self, args):
        pass

    def __init__(self, message=None, **kwargs):
        print("replies.py __init__ target " + message.target)

        if message and "source" not in kwargs:
            kwargs["source"] = message.target

        if message and "target" not in kwargs:
            kwargs["target"] = message.source

        if 'time' not in kwargs:
            kwargs["time"] = int(time.time())

        # if 'content' not in kwargs:
        # kwargs["content"] = "Hello, stranger."

        args = defaultdict(str)
        for k, v in kwargs.items():
            if is_string(v):
                v = to_text(v)
            args[k] = v
        self.process_args(args)
        self._args = args

    def render(self):
        return to_text(self.TEMPLATE.format(**self._args))

    def __getattr__(self, item):
        if item in self._args:
            return self._args[item]


class TextReply(WeChatReply):
    TEMPLATE = to_text(
        """
        <xml>
        <ToUserName><![CDATA[{target}]]></ToUserName>
        <FromUserName><![CDATA[{source}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
        </xml>
        """
    )


class SuccessReply(object):
    def render(self):
        return "success"


def process_function_reply(reply, message=None):
    if is_string(reply):
        print(TAG + " source " + message.source + " reply " + reply)
        return TextReply(message=message, content=reply)