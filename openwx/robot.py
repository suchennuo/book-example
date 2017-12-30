from . import utils
import six
import warnings

from .parser import parse_xml, process_message
from openwx.config import ConfigAttribute, Config
from openwx.replies import process_function_reply
from openwx.client import Client
from openwx.exceptions import ConfigError
from openwx.utils import (
    to_binary, to_text, cached_property,
)

from inspect import signature
"""
class dict(**kwarg)
eg:
dict() # 空字典
class dict(mapping, **kwarg)
eg:
dict(a='a', b='b') #传入关键字
class dict(iterable, **kwarg)
eg:
dict([('one', 1), ('tow', 2)]) #可迭代对象来构造字典

"""
# 传入关键字
_DEFAULT_CONFIG = dict(
    TOKEN=None,
    APP_ID=None,
    APP_SPECRET=None,
    ENCODING_AES_KEY=None
)

__all__ = ['BaseRoBot', 'WeRoBot']

# 获取自定义的函数注解

"""
函数注解 可以让定义函数的时候对参数和返回值添加注解
类型检查，获取参数顺序以及函数注解，可以通过装饰器来检查

装饰器的用处：https://wiki.python.org/moin/PythonDecoratorLibrary
1. 注入参数 （提供默认参数，生成参数）
2. 记录函数行为 （log, cache, count...)
3. pre/post 处理 (配置上下文...)
4. 修改调用时的上下文 (异步线程，并发，类方法）

"""


class BaseRobot(object):

    message_types = ['text', 'image', 'unknown']
    token = ConfigAttribute("TOKEN")

    def __init__(self, token=None, app_id=None, app_secret=None, encoding_aes_key=None,
                 config=None, **kwargs):
        # 函数注解
        # 验证函数参数是否合法
        self._handlers = {k: [] for k in self.message_types}
        self._handlers['all'] = []

        if config is None:
            self.config = Config(_DEFAULT_CONFIG)
            # 更新字典
            self.config.update(
                TOKEN=token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
                ENCODING_AES_KEY=encoding_aes_key,
                SESSION_STORAGE=None
            )

            for k, v in kwargs.items():#获取函数参数注解
                self.config[k.upper()] = v

        else:
            self.config = config

        self.use_encryption = False

    @cached_property
    def crypto(self):
        app_id = self.config.get("APP_ID", None)
        if not app_id:
            raise ConfigError("You need to provide app_id to encrypt/decrypt message")

        encoding_aes_key = self.config.get("ENCODING_AES_KEY", None)

        if not encoding_aes_key:
            raise ConfigError("You need to provide encoding_aes_key to encrypt/decrypt messages")

        self.use_encryption = False

        from .crypto import MessageCrypt
        return MessageCrypt(
            token=self.config["TOKEN"],
            encoding_aes_key=encoding_aes_key,
            app_id=app_id
        )

    @cached_property
    def client(self):
        return Client(self.config)

    @cached_property
    def session_storage(self):
        if self.config["SESSION_STORAGE"] is False:
            return None

    def handler(self, f):
        self.add_handler(f, type='all')
        return f

    def text(self, f):
        """
        为文本添加一个 handler 方法的装饰器
        :param f:
        :return:
        """
        self.add_handler(f, type='text')
        return f

    def add_handler(self, func, type='all'):
        """
        为 BaseRobot 实例添加一个 handler

        :param func: 要作为 handler 的方法
        :param type: handler 种类
        :return: None
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))

        self._handlers[type].append((func, len(signature(func).parameters.keys())))

    def get_handlers(self, type):
        return self._handlers.get(type, []) + self._handlers['all']

    def parse_message(self, body, timestamp=None, nonce=None, msg_signature=None):
        """
        解析 raw xml, 如果需要的话，进行解密 返回 robot message
        :param body: 微信发来的请求中的 Body

        :return: robot message
        """
        message_dic = parse_xml(body)

        if "Encrypt" in message_dic:
            #TODO: 解密 raw message
            pass;
        return process_message(message_dic)

    def get_reply(self, message):

        """
        根据 message 内容获取 reply 对象

        :param message:
        :return:
        """
        session_storage = self.session_storage

        id = None
        session = None
        if session_storage and hasattr(message, "source"):
            id = to_binary(message.source)
            session = session_storage[id]
        print("message type " + message.type)
        handlers = self.get_handlers(message.type)
        # print(*handlers, sep='\n')  # nothing
        print("message source " + message.source)
        return process_function_reply('text', message=message)

        # try:
        #     for handler, args_count in handlers:
        #         args = [message, session][:args_count]
        #         reply = handler(*args)
        #         if session_storage and id:
        #             session_storage[id] = session
        #         if reply:
        #             return process_function_reply(reply, message=message)
        # except:
        #     print("Catch an exception")

    def get_encrypted_reply(self, message):
        """
        对一个指定的 WeRobot message 获取 handlers 处理后得到的 Reply
        如有必要，对 reply 进行加密
        返回 reply render 后的文本
        :param self:
        :param message: WeRoBot Message 实例
        :return:
        """
        reply = self.get_reply(message)
        if not reply:
            return ''
        # if self.user_encryption:
        #     return ''
        else:
            print(reply.render())
            return reply.render()


class WeChatRobot(BaseRobot):
    pass