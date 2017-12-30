
from openwx import robot
from openwx.robot import WeChatRobot, BaseRobot

request_mock = "<xml><ToUserName><![CDATA[gh_139fe4dae70c]]></ToUserName>" \
               "<FromUserName><![CDATA[ofK091hnGW1lb396t4ak8vemvyJI]]></FromUserName>" \
               "<CreateTime>1514618199</CreateTime>" \
               "<MsgType><![CDATA[text]]></MsgType>" \
               "<Content><![CDATA[看]]></Content>" \
               "<MsgId>6505235631078416834</MsgId>" \
               "</xml>"
if __name__ == '__main__':


    robot = robot.WeChatRobot()



    pass