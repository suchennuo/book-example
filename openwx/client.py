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
    """
    微信 API 操作类
    主动发信息，创建自定义菜单等
    """

    def __init__(self, config):
        self.config = config
        self._token = None
        self.token_expires_at = None

    @property
    def appid(self):
        return self.config.get("APP_ID", None)

    @property
    def appsecret(self):
        return self.config.get("APP_SECRET", None)

    @property
    def token(self):
        return self.get_access_token()


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
        print("response json {}".format(json))
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
        print("grant_token {} {} ".format(self.appid, self.appsecret))
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
            print("token expires {}".format(self.token_expires_at))
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

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息
        :param user_id:
        :param media_id:
        :return:
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser":user_id,
                "msgtype":"image",
                "image":{
                    "media_id":media_id
                }
            }
        )

    def get_user_info(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息
        :param user_id:
        :param lang:
        :return:
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/user/info",
            params={
                "access_token": self.token,
                "openid": user_id,
                "lang": lang
            }
        )


    def create_menu(self, menu_data):

        """

        :param menu_data: python 字典
        :return:
        """

        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/menu/create",
            data=menu_data
        )

    def create_custom_menu(self, menu_data, matchrule):
        return self.post(
            url="http://api.weixin.qq.com/cgi-bin/menu/addconditional",
            data={
                "button": menu_data,
                "matchrule": matchrule
            }
        )

