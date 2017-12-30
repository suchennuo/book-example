# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from hashlib import sha1
import six
from functools import wraps
import io
import json
import random
import os
import string
import time
import re
from secrets import choice

string_types = (six.string_types, six.text_type, six.binary_type)

re_type = type(re.compile("regex_test"))

def check_signature(token, timestamp, nonce, signature):
    if not (token and timestamp and nonce and signature):
        return False
    sign = get_signature(token, timestamp, nonce)
    return sign == signature


def get_signature(token, timestamp, nonce, *args):
    #可变传参
    sign = [token, timestamp, nonce] + list(args)
    sign.sort()
    sign = to_binary(''.join(sign))
    return sha1(sign).hexdigest()


def to_binary(value, encoding="utf-8"):
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


def to_text(value, encoding="utf-8"):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def check_token(token):
    return re.match('^[A-Za-z0-9]{3,32}$', token)


def is_string(value):
    return isinstance(value, string_types)

"""
format 通过{} 和 : 来代替 %

python 参考手册中的例子：
eg:

def _square(x):
    return x*x

square = trace(_square)
被装饰的原函数会变成另一个函数，函数名和函数doc都会发生变化，wraps 消除这种影响
可以保留原函数的名称和docstring


class property(fget[, fset[, fdel[, doc]]])
检查输入类型，控制读写权限
"""

def cached_property(method):
    prop_name = '_{}'.format(method.__name__)

    @wraps(method)
    # 如果不加这句，返回的将是 wrapped_func, 而不是 method.__name__
    def wrapped_func(self, *args, **kwargs):
        if not hasattr(self, prop_name):  # 判断 self 是否含有 prop_name 属性
            setattr(self, prop_name, method(self, *args, **kwargs))
            # 和 getattr 对应，设置属性值
            # 设置 prop_name = method 的执行结果
        return getattr(self, prop_name)
    return property(wrapped_func)  # 返回属性值, 只读
    # 为毛不直接返回 wrapped_func




