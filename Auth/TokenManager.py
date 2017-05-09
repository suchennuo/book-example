
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re
from django.conf import settings as django_settings
"""
注意事项：
    encodebytes error: expected bytes-like object, not str
    只有使用相同 salt 的 serializer 才能把值加载出来
"""

class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('utf-8'))

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key, self.salt)
        return serializer.dumps(username)

    # 验证 token 过期
    def confirm_validate_token(self, token, expiration=600):
        serializer = utsr(self.security_key, self.salt)
        return serializer.loads(token, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key, self.salt)
        return serializer.loads(token)

token_confirm = Token(django_settings.SECRET_KEY) #

"""
拓展：
    Best way to convert String to bytes in Python 3 ?
    http://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3

    itsdangerous 参考 http://itsdangerous.readthedocs.io/en/latest/
    Python 中使用 pickle 持久化对象 https://blog.oldj.net/2010/05/26/python-pickle/
    pickle 模块将对象转化为文件保存在磁盘上，需要的时候在读取还原

"""
