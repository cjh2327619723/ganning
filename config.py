import os

MAIL_DEBUG = True  # 开启debug，便于调试看信息
MAIL_SUPPRESS_SEND = False  # 发送邮件，为True则不发送
MAIL_SERVER = 'smtp.qq.com'  # 邮箱服务器
MAIL_PORT = 465  # 端口
MAIL_USE_SSL = True  # 重要，qq邮箱需要使用SSL
MAIL_USE_TLS = False  # 不需要使用TLS
MAIL_USERNAME = '2646489146@qq.com'  # 填邮箱
MAIL_PASSWORD = 'axvjileawrfdeahd'  # 填授权码
FLASK_MAIL_SENDER = '浩奇公司<2646489146@qq.com>'  # 邮件发送方
FLASK_MAIL_SUBJECT_PREFIX = '培训通知'  # 邮件标题
MAIL_DEFAULT_SENDER = '2646489146@qq.com'  # 填邮箱，默认发送者**加粗样式**
SECRET_KEY = os.urandom(24)
