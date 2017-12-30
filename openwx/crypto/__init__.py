import base64

import socket
import struct
import time

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend

class PrpCrypto(object):
    """
    提供接收和推送给公众平台消息的加解密接口
    """
    pass


class MessageCrypt(object):
    ENCRYPTED_MESSAGE_XML = """
    <xml>
    <Encrypt><![CDATA[{encrypt}]]></Encrypt>
    <MsgSignature><![CDATA[{signature}]]></MsgSignature>
    <TimeStamp>{timestamp}</TimeStamp>
    <Nonce><![CDATA[{nonce}]]></Nonce>
    </xml>
    """.strip()

    def __init__(self, token, encoding_aes_key, app_id):
        pass
