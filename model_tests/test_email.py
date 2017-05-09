import smtplib
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.core.mail import send_mail

fromaddr = "superlist@yongchaozhang.com"#prompt("From: ")
toaddrs  = "550906133@qq.com" #prompt("To: ").split()
subject  = "Hi"#prompt("Subject: ")

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddrs
msg['Subject'] = subject
msg.attach(MIMEText("A test email from django.", "plain", "utf-8"))

#添加图片附件
with open('/Users/alpha/Documents/homework_share_icon.png', 'rb') as f:
    mime = MIMEBase("image", "png", filename="homework_share_icon.png")
    mime.add_header("Content-Disposition", "attchment", filename="homework_share_icon.png")
    mime.add_header("Content-ID", "<0>")
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msg.attach(mime)

# 如果是其他的服务，只需要更改 host 为对应地址，port 对对应端口即可
server = smtplib.SMTP_SSL(host='smtp.exmail.qq.com', port=465)
server.set_debuglevel(1)    # 开启调试，会打印调试信息
print("--- Need Authentication ---")
server.login('superlist@yongchaozhang.com', 'Tsil@1122')
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()

# send_mail("django say", "stay hungry, stay foolish", "superlist@yongchaozhang.com",
#           ['550906133@qq.com'], fail_silently=False, auth_user="superlist@yongchaozhang.com",
#           auth_password="Tsil@1122")