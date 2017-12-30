import time
import requests

from requests.compat import json as _json

from openwx.utils import to_text

"""
requests
"""

class ClientException(Exception):
    pass

def check_error(json):
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    return json

class Client(object):

    def __init__(self, config):
        self.config = config
        self.token = None
        self.token_expires_at = None

    @property
    def appid(self):
        return self.config.get("APP_ID", None)

    @property
    def appsecret(self):
        return self.config.get("APP_SECRET", None)



    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            # ensure_ascii 默认 true ,会对所有 非 ASCII 转义
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()  # 检查请求是否成功
        r.encoding = "utf-8"
        json = r.json()
        if check_error(json):
            return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def grant_token(self):
        """
        获取 access token
        :return:
        """

        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type":"client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    def get_access_token(self):
        """
        判断现有token是否过期。
        需要多进程或者多机器部署需要重写这个函数来自定义 token 的存储，刷新测量
        :return:
        """

        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.grant_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token

    def send_text_message(self, user_id, content):
        """
        发送文本消息
        :param user_id:
        :param content:
        :return: 返回的 Json 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "text",
                "text": {"content": content}
            }
        )

