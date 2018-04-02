# encoding=utf-8

import smtplib
import traceback
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import io
import tushare as ts
from General.GlobalSetting import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure




'''''
@subject:邮件主题
@msg:邮件内容
@toaddrs:收信人的邮箱地址
@fromaddr:发信人的邮箱地址
@smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com

@password:发信人的邮箱密码
'''


def sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password):

    mail_msg = MIMEMultipart()
    if not isinstance(subject, str):
        subject = str(subject, 'utf-8')

    mail_msg['Subject'] = subject
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg,'html','utf-8'))

    # buf = io.BytesIO()
    #
    # fig = Figure()
    # canvas = FigureCanvas(fig)
    # ax = fig.gca()
    #
    # ax.text(0.0,0.0,"test",fontsize=45)
    # ax.axis('off')
    # canvas.draw()
    # image = np.fromstring(canvas.tostring_rgb(),dtype='uint8')
    # plt.savefig(buf,format='png')
    # buf.seek(0)
    #
    # msgImage = MIMEImage(buf.read())
    #
    # msgImage.add_header('Content-ID', '<image1>')
    # mail_msg.attach(msgImage)

    # # jpg类型的附件
    # msgImage = MIMEImage(plt.figimage)
    # jpgpart = MIMEApplication(plt.figure())
    # msgImage.add_header('Content-Disposition', 'attachment', filename='beauty.jpg')
    # mail_msg.attach(image)


    # buf = io.BytesIO()
    # plt.figure()
    # plt.savefig(buf,format='png')
    # buf.seek(0)

    # msgImage = MIMEImage(buf.read())
    f = open("C:/Users/paul/Desktop/test.png",'rb')


    mime = MIMEImage(f.read())
    mime.add_header('Content-ID','<0>')
    mime.add_header('X-Attachment-Id','0')
    mime.add_header('Content-Disposition','attachment',filename='test.png')
    # mime.set_payload(f.read())

    # file1 = "C:\\hello.jpg"
    # image = MIMEImage(open(file1, 'rb').read())
    # image.add_header('Content-ID', '<image1>')
    # msg.attach(image)

    # encoders.encode_base64(mime)
    mail_msg.attach(mime)

    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)             # 连接smtp服务器
        s.login(fromaddr, password)     # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()
    except :
        print("Error: unable to send email")
        print(traceback.format_exc())


if __name__ == '__main__':
    fromaddr = "pwnevy@163.com"
    # fromaddr = "ai_report@163.com"
    smtpaddr = "smtp.163.com"

    toaddrs = ["1210055099@qq.com"]
    subject = "AI自动报告-V1"
    password = "87315287"
    # password = "ypw1989"
    # msg = ts.get_latest_news(top=5,show_content=True).loc[0,"content"]
    # msg = '<html><body><h1>Hello</h1>' +\
    #       '<p><img src = "cid:0"></p>' +\
    #     '</body></html>'

    msg = '<html><body><h1>Hello</h1><p>img src = "cid:0"</p></body></html>'


    sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password)
