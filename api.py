# -*- coding: utf-8 -*-
import cgi
import csv
import io
import json
import random
import time
from datetime import datetime
from flask_mail import Mail, Message
import MySQLdb
import flask
from flask import request, render_template, Response, redirect, session
from flask_cors import CORS
import config

# 创建Flask对象
server = flask.Flask(__name__)
# 解决跨域问题
CORS(server, supports_credentials=True)
# 连接数据库
db = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='homework')
mail = Mail()
# 引入加载配置
server.config.from_object(config)
mail.init_app(server)
server.executorID = ""


# 登录
@server.route('/login', methods=['POST'])
def login():
    post_data = json.loads(request.get_data(as_text=True))
    radios = post_data['radios']
    # 经理登录
    if radios == "A":
        try:
            cursor = db.cursor()
            number = cursor.execute('SELECT password FROM manager WHERE username="%s"' % post_data['username'])
            if number == 0:
                dic = {
                    "status": 1,
                    "msg": "账号或者密码错误！",
                    "data": {}
                }
                return json.dumps(dic)
            else:
                password = cursor.fetchall()[0][0]
        except Exception as e:
            dic = {
                "status": 2,
                "msg": str(e),
                "data": {}
            }
            return json.dumps(dic)
        if post_data['password'] == password:
            dic = {
                "status": 0,
                "msg": "登录成功！",
                "data": {
                    "type": 0
                }
            }
            return json.dumps(dic)
        else:
            dic = {
                "status": 1,
                "msg": "账号或者密码错误！",
                "data": {}
            }
            return json.dumps(dic)
    else:
        try:
            cursor = db.cursor()
            number = cursor.execute('SELECT password FROM executor WHERE username="%s"' % post_data['username'])
            if number == 0:
                dic = {
                    "status": 1,
                    "msg": "账号或者密码错误！",
                    "data": {}
                }
                return json.dumps(dic)
            else:
                password = cursor.fetchall()[0][0]
        except Exception as e:
            dic = {
                "status": 2,
                "msg": str(e),
                "data": {}
            }
            return json.dumps(dic)
        if post_data['password'] == password:
            dic = {
                "status": 0,
                "msg": "登录成功！",
                "data": {
                    "type": 1
                }
            }
            # 存储cookies
            cursor = db.cursor()
            cursor.execute('SELECT id FROM executor WHERE username="%s" AND password="%s"' %
                           (post_data['username'], post_data['password']))
            executorID = cursor.fetchall()[0][0]
            session['executorID'] = str(executorID)
            return json.dumps(dic)
        else:
            dic = {
                "status": 1,
                "msg": "账号或者密码错误！",
                "data": {}
            }
            return json.dumps(dic)


# 获取公司申请
@server.route("/getCompanyApply", methods=["GET"])
def getCompanyApply():
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM companyapply')
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "companyApplyID": raw_data[i][0],
                "companyName": raw_data[i][1],
                "field": raw_data[i][2],
                "email": raw_data[i][3],
                "state": raw_data[i][4],
                "applyTime": raw_data[i][5]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 修改公司申请
@server.route('/changeCompanyApply', methods=['POST'])
def changeCompanyApply():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute(
            'UPDATE companyapply SET companyName="%s",field="%s",email="%s" WHERE companyApplyID="%d"' %
            (post_data['companyName'], post_data['field'], post_data['email'], post_data['companyApplyID']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "修改成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 删除公司申请
@server.route('/deleteCompanyApply', methods=['POST'])
def deleteCompanyApply():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM companyapply WHERE companyApplyID="%d"' % post_data['companyApplyID'])
        db.commit()
        dic = {
            "status": 0,
            "msg": "删除成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 获取执行人信息
@server.route("/getExecutor", methods=["GET"])
def getExecutor():
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM executor')
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "id": raw_data[i][0],
                "username": raw_data[i][1],
                "password": raw_data[i][2],
                "executorName": raw_data[i][3]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 修改执行人信息
@server.route('/changeExecutor', methods=['POST'])
def changeExecutor():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute(
            'UPDATE executor SET executorName="%s",username="%s",password="%s" WHERE id="%d"' %
            (post_data['executorName'],
             post_data['username'],
             post_data['password'],
             post_data['id']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "修改成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 删除执行人信息
@server.route("/deleteExecutor", methods=["POST"])
def deleteExecutor():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM executor WHERE id="%d"' % int(post_data['executorID']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "删除成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 添加执行人信息
@server.route('/addExecutor', methods=['POST'])
def addExecutor():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO executor (username,password,executorName) VALUES'
                       ' ("%s","%s","%s")' %
                       (post_data['username'],
                        post_data['password'],
                        post_data['executorName']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "添加成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 验证执行人ID
@server.route("/verifyExecutor", methods=["POST"])
def verifyExecutor():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM executor WHERE id="%d"' % int(post_data['executorID']))
        if number == 0:
            dic = {
                "status": 422,
                "errors": "此ID无效！"
            }
        else:
            dic = {
                "status": 0
            }
    except Exception as e:
        dic = {
            "status": 422,
            "errors": str(e)
        }
    return dic


# 获取教师信息
@server.route("/getTeacher", methods=["GET"])
def getTeacher():
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM teacher')
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "teacherID": raw_data[i][0],
                "teacherName": raw_data[i][1],
                "teacherTitle": raw_data[i][2],
                "teacherField": raw_data[i][3],
                "teacherEmail": raw_data[i][4],
                "teacherPhone": raw_data[i][5]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 修改教师信息
@server.route('/changeTeacher', methods=['POST'])
def changeTeacher():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute(
            'UPDATE teacher SET teacherName="%s",teacherTitle="%s",teacherField="%s",teacherEmail="%s",teacherPhone="%s" WHERE teacherID="%d"' %
            (post_data['teacherName'],
             post_data['teacherTitle'],
             post_data['teacherField'],
             post_data['teacherEmail'],
             post_data['teacherPhone'],
             post_data['teacherID']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "修改成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 删除教师信息
@server.route("/deleteTeacher", methods=["POST"])
def deleteTeacher():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM teacher WHERE teacherID="%d"' % post_data['teacherID'])
        db.commit()
        dic = {
            "status": 0,
            "msg": "删除成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 添加教师信息
@server.route('/addTeacher', methods=['POST'])
def addTeacher():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO teacher (teacherName,teacherTitle,teacherField,teacherEmail,teacherPhone) VALUES'
                       ' ("%s","%s","%s","%s","%s")' %
                       (post_data['teacherName'],
                        post_data['teacherTitle'],
                        post_data['teacherField'],
                        post_data['teacherEmail'],
                        post_data['teacherPhone']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "添加成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 验证教师ID
@server.route("/verifyTeacher", methods=["POST"])
def verifyTeacher():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM teacher WHERE teacherID="%d"' % int(post_data['teacherID']))
        if number == 0:
            dic = {
                "status": 422,
                "errors": "此ID无效！"
            }
        else:
            dic = {
                "status": 0
            }
    except Exception as e:
        dic = {
            "status": 422,
            "errors": str(e)
        }
    return dic


# 经理操作
@server.route('/processCourse', methods=['POST'])
def processCourse():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        # 创建课程
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO course (executorID,teacherID,courseName,companyApplyID,startTime,endTime,courseContent,field,coursePlace,free) VALUES'
            '("%d","%d","%s","%d","%s","%s","%s","%s","%s","%d")' %
            (int(post_data['executorID']),
             int(post_data['teacherID']),
             post_data['courseName'],
             int(post_data['companyApplyID']),
             datetime.utcfromtimestamp(int(post_data['startTime'])),
             datetime.utcfromtimestamp(int(post_data['endTime'])),
             post_data['courseContent'],
             post_data['field'],
             post_data['coursePlace'],
             int(post_data['free'])))
        db.commit()
        cursor = db.cursor()
        cursor.execute('UPDATE companyapply SET state="%s" WHERE companyApplyID="%d"' %
                       ("已同意", int(post_data['companyApplyID'])))
        db.commit()
        dic = {
            "status": 0,
            "msg": "新建课程成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 根据执行人的ID获取课程信息
@server.route("/getCourseForExecutor", methods=["GET"])
def getCourseForExecutor():
    executorID = int(session['executorID'])
    print(executorID)
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM course WHERE executorID="%d"' % executorID)
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "courseID": raw_data[i][0],
                "executorID": raw_data[i][1],
                "teacherID": raw_data[i][2],
                "companyApplyID": raw_data[i][3],
                "courseName": raw_data[i][4],
                "courseContent": raw_data[i][5],
                "field": raw_data[i][6],
                "startTime": raw_data[i][7],
                "endTime": raw_data[i][8],
                "coursePlace": raw_data[i][9],
                "free": raw_data[i][10],
                "courseState": raw_data[i][11]
            })
        for _ in _data:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM teacher WHERE teacherID="%d"' % _['teacherID'])
            info_teacher = cursor.fetchall()[0]
            _['teacherName'] = info_teacher[1]
            _['teacherTitle'] = info_teacher[2]
            _['teacherField'] = info_teacher[3]
            _['teacherEmail'] = info_teacher[4]
            _['teacherPhone'] = info_teacher[5]
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 验证课程ID
@server.route("/verifyCourseIDWithExecutorID", methods=["POST"])
def verifyCourseIDWithExecutorID():
    post_data = json.loads(request.get_data(as_text=True))
    executorID = int(session['executorID'])
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM course WHERE executorID="%d" and courseID="%d"' %
                                (executorID, int(post_data['courseID'])))
        if number == 0:
            dic = {
                "status": 422,
                "errors": "此ID无效！"
            }
        else:
            dic = {
                "status": 0
            }
    except Exception as e:
        dic = {
            "status": 422,
            "errors": str(e)
        }
    return dic


# 执行人登录
@server.route('/executorLogin', methods=['POST'])
def executorLogin():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT password FROM executor WHERE username="%s"' % post_data['username'])
        if number == 0:
            dic = {"code": 205, "data": {"message": "账号或者密码错误！"}}
            return json.dumps(dic)
        else:
            password = cursor.fetchall()[0][0]
    except Exception as e:
        dic = {"code": 400, "error_message": str(e)}
        return json.dumps(dic)
    if post_data['password'] == password:
        dic = {"code": 201}
    else:
        dic = {"code": 204, "data": {"message": "账号或者密码错误！"}}
    return json.dumps(dic)


# 根据课程ID获取报名表
@server.route("/getEntryformByCourseID", methods=["POST"])
def getEntryformByCourseID():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM entryform WHERE courseID="%d"' % int(post_data['courseID']))
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "entryformID": raw_data[i][0],
                "isCompany": raw_data[i][2],
                "studentName": raw_data[i][3],
                "studentSex": raw_data[i][4],
                "studentCompany": raw_data[i][5],
                "studentField": raw_data[i][6],
                "studentLevel": raw_data[i][7],
                "studentEmail": raw_data[i][8],
                "entryformState": raw_data[i][9],
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 改变报名表状态
@server.route("/changeEntryformState", methods=["POST"])
def changeEntryformState():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('UPDATE entryform SET entryformState="%s" WHERE entryformID="%d"' %
                       (post_data['entryformState'], int(post_data['entryformID'])))
        db.commit()
        dic = {
            "status": 0,
            "msg": "操作成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 发送培训通知
@server.route("/sendCourseInfo", methods=["POST"])
def sendCourseInfo():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM course WHERE courseID="%d"' % int(post_data['courseID']))
        raw_data = cursor.fetchall()
        courseInfo = {
            "课程名称": raw_data[0][4],
            "课程内容": raw_data[0][5],
            "课程方向": raw_data[0][6],
            "开始时间": raw_data[0][7],
            "结束时间": raw_data[0][8],
            "培训地点": raw_data[0][9],
            "培训费用": raw_data[0][10],
            "teacherID": raw_data[0][2],
        }
        cursor = db.cursor()
        cursor.execute('SELECT * FROM teacher WHERE teacherID="%d"' % int(courseInfo['teacherID']))
        info_teacher = cursor.fetchall()[0]
        courseInfo['教师姓名'] = info_teacher[1]
        courseInfo['教师职称'] = info_teacher[2]
        courseInfo['教师方向'] = info_teacher[3]
        # 邮件正文,后续改写成html
        body = (
            f"你好，这里是浩奇公司培训通知，我们将要推出如下的新课程，如果您感兴趣请进入http://127.0.0.1:5500/receiveEntryform.html\n"
            f"课程ID:{post_data['courseID']}\n"
            f"课程名称:{courseInfo['课程名称']}\n"
            f"课程内容:{courseInfo['课程内容']}\n"
            f"开始时间:{courseInfo['开始时间']}\n"
            f"结束时间:{courseInfo['结束时间']}\n"
            f"培训地点:{courseInfo['培训地点']}\n"
            f"培训费用:{courseInfo['培训费用']}\n"
            f"教师名字:{courseInfo['教师姓名']}\n"
            f"教师职称:{courseInfo['教师职称']}\n"
            f"教师方向:{courseInfo['教师方向']}")
        # 邮箱地址字符串列表
        recipients = []
        cursor = db.cursor()
        number = cursor.execute('SELECT studentEmail FROM entryform')
        raw_data = cursor.fetchall()
        for i in range(number):
            recipients.append(raw_data[i][0])
        if recipients:
            message = Message(subject='培训通知', recipients=recipients, body=body)
            mail.send(message)
        dic = {
            "status": 0,
            "msg": "发送成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 接收报名表
@server.route("/receiveEntryform", methods=["POST"])
def receiveEntryform():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO entryform (courseID,isCompany,studentName,studentSex,studentCompany,studentField,studentLevel,studentEmail) VALUES'
            ' ("%d","%s","%s","%s","%s","%s","%s","%s")' %
            (int(post_data['courseID']),
             post_data['isCompany'],
             post_data['studentName'],
             post_data['studentSex'],
             post_data['studentCompany'],
             post_data['studentField'],
             post_data['studentLevel'],
             post_data['studentEmail']))
        db.commit()
        body = f"你好，{post_data['studentName']}同学，您已经成功报名本课程，请按时完成学习任务！\n"
        message = Message(subject='培训通知', recipients=[f"{post_data['studentEmail']}"], body=body)
        mail.send(message)
        dic = {
            "status": 0,
            "msg": "报名成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 开课
@server.route("/openCourse", methods=["POST"])
def openCourse():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM comeandpay WHERE courseID="%d"' % int(post_data['courseID']))
        if number > 0:
            dic = {
                "status": 1,
                "msg": "不能重复开课！",
                "data": {}
            }
        else:
            cursor = db.cursor()
            cursor.execute('UPDATE course SET courseState="%s" WHERE courseID="%d"' %
                           ("pending", int(post_data['courseID'])))
            db.commit()
            cursor = db.cursor()
            number = cursor.execute(
                'SELECT entryformID,isCompany,studentEmail FROM entryform WHERE courseID="%d" AND entryformState="%s"' %
                (int(post_data['courseID']), "同意报名"))
            raw_data = cursor.fetchall()
            data = []
            recipients = []

            for i in range(number):
                data.append(
                    {
                        "entryformID": raw_data[i][0],
                        "isCompany": raw_data[i][1]}
                )
                recipients.append(raw_data[i][2])
            for _data in data:
                if _data['isCompany'] == "是":
                    cursor = db.cursor()
                    cursor.execute(
                        'INSERT INTO comeandpay (entryformID,isPayed,courseID) VALUES ("%d","%s","%d")' %
                        (_data['entryformID'], "是", int(post_data['courseID'])))
                    db.commit()
                else:
                    cursor = db.cursor()
                    cursor.execute(
                        'INSERT INTO comeandpay (entryformID,courseID) VALUES ("%d","%d")' %
                        (_data['entryformID'], int(post_data['courseID'])))
                    db.commit()
            body = f"您报名的培训课程即将开课，请按时参加！\n"
            message = Message(subject='培训提醒', recipients=recipients, body=body)
            mail.send(message)
            dic = {
                "status": 0,
                "msg": "操作成功！",
                "data": {}
            }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 获取签到页面的数据
@server.route("/getComeAndPay", methods=["POST"])
def getComeAndPay():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM comeandpay WHERE courseID="%d"' % int(post_data['courseID']))
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            entryformID = int(raw_data[i][1])
            cursor = db.cursor()
            cursor.execute('SELECT studentName FROM entryform WHERE entryformID="%d"' % entryformID)
            studentName = cursor.fetchall()[0][0]
            _data.append({
                "id": raw_data[i][0],
                "studentName": studentName,
                "isPayed": raw_data[i][2],
                "isCome": raw_data[i][3]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 签到
@server.route("/changeCome", methods=["POST"])
def changeCome():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('UPDATE comeandpay SET isCome="%s" WHERE id="%d"' %
                       ("是", int(post_data['id'])))
        db.commit()
        dic = {
            "status": 0,
            "msg": "操作成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 缴费
@server.route("/changePay", methods=["POST"])
def changePay():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('UPDATE comeandpay SET isPayed="%s" WHERE id="%d"' %
                       ("是", int(post_data['id'])))
        db.commit()
        dic = {
            "status": 0,
            "msg": "操作成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 结课
@server.route("/closeCourse", methods=["POST"])
def closeCourse():
    post_data = json.loads(request.get_data(as_text=True))
    courseID = int(post_data['courseID'])
    try:
        cursor = db.cursor()
        cursor.execute('SELECT courseState FROM course WHERE courseID="%d"' % int(post_data['courseID']))
        courseState = cursor.fetchall()[0][0]
        if courseState == "1":
            dic = {
                "status": 1,
                "msg": "该课程已结束！",
                "data": {}
            }
        else:
            cursor = db.cursor()
            cursor.execute('UPDATE course SET courseState="%s" WHERE courseID="%d"' %
                           ("1", courseID))
            db.commit()
            cursor = db.cursor()
            number = cursor.execute('SELECT entryformID FROM comeandpay WHERE courseID="%d" AND isPayed="%s"' %
                                    (courseID, "是"))
            raw_data = cursor.fetchall()
            entryformID = []
            for i in range(number):
                entryformID.append(int(raw_data[i][0]))
            recipients = []
            for _entryformID in entryformID:
                cursor = db.cursor()
                cursor.execute('SELECT studentEmail FROM entryform WHERE entryformID="%d"' % _entryformID)
                recipients.append(cursor.fetchall()[0][0])
            body = f"您的参加的课程ID为{courseID}的培训课程已经结课，恳请您完成课程调查问卷:http://127.0.0.1:5500/questionnaire.html"
            message = Message(subject='填写课程调查问卷', recipients=recipients, body=body)
            mail.send(message)
            dic = {
                "status": 0,
                "msg": "操作成功！",
                "data": {}
            }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 接收报名表
@server.route("/receiveQuestionnaire", methods=["POST"])
def receiveQuestionnaire():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO questionnaire (courseID,teacherScore,courseScore,executorScore,comment) VALUES'
            ' ("%d","%d","%d","%d","%s")' %
            (int(post_data['courseID']),
             int(post_data['teacherScore']),
             int(post_data['courseScore']),
             int(post_data['executorScore']),
             post_data['comment']))
        db.commit()
        dic = {
            "status": 0,
            "msg": "提交成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 校验课程ID
@server.route("/verifyCourseID", methods=["POST"])
def verifyCourseID():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM course WHERE courseID="%d"' % int(post_data['courseID']))
        if number == 0:
            dic = {
                "status": 422,
                "errors": "该课程ID无效！"
            }
        else:
            dic = {
                "status": 0
            }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 获取签到页面的数据
@server.route("/getQuestionnaire", methods=["POST"])
def getQuestionnaire():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM questionnaire WHERE courseID="%d"' % int(post_data['courseID']))
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "questionnaireID": raw_data[i][0],
                "teacherScore": raw_data[i][2],
                "courseScore": raw_data[i][3],
                "executorScore": raw_data[i][4],
                "comment": raw_data[i][5]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 生成汇总表
@server.route("/makeSummary", methods=["POST"])
def makeSummary():
    post_data = json.loads(request.get_data(as_text=True))
    courseID = int(post_data['courseID'])
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM summary WHERE courseID="%d"' % courseID)
        if number != 0:
            dic = {
                "status": 1,
                "msg": "不可重复生成汇总表！",
                "data": {}
            }
        else:
            cursor = db.cursor()
            number = cursor.execute('SELECT * FROM questionnaire WHERE courseID="%d"' % courseID)
            raw_data = cursor.fetchall()
            teacherScore = []
            courseScore = []
            executorScore = []
            for i in range(number):
                teacherScore.append(int(raw_data[i][2]))
                courseScore.append(int(raw_data[i][3]))
                executorScore.append(int(raw_data[i][4]))
            _teacherScore = sum(teacherScore) / len(teacherScore)
            _courseScore = sum(courseScore) / len(courseScore)
            _executorScore = sum(executorScore) / len(executorScore)
            cursor = db.cursor()
            cursor.execute('SELECT free FROM course WHERE courseID="%d"' % courseID)
            free = cursor.fetchall()[0][0]
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO summary (courseID,teacherScore,courseScore,executorScore,totalStudent,money) VALUES'
                ' ("%d","%f","%f","%f","%d","%d")' %
                (courseID,
                 _teacherScore,
                 _courseScore,
                 _executorScore,
                 len(teacherScore),
                 len(teacherScore) * free))
            db.commit()
            dic = {
                "status": 0,
                "msg": "操作成功！",
                "data": {}
            }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 汇总表
@server.route("/getSummary", methods=["POST"])
def getSummary():
    post_data = json.loads(request.get_data(as_text=True))
    executorID = 14
    courseID = int(post_data['courseID'])
    try:
        cursor = db.cursor()
        number = cursor.execute('SELECT * FROM summary WHERE courseID="%d"' % courseID)
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            cursor = db.cursor()
            cursor.execute('SELECT courseName FROM course WHERE courseID="%d"' % courseID)
            courseName = cursor.fetchall()[0][0]
            _data.append({
                "summaryID": raw_data[i][0],
                "courseName": courseName,
                "teacherScore": raw_data[i][2],
                "courseScore": raw_data[i][3],
                "executorScore": raw_data[i][4],
                "totalStudent": raw_data[i][5],
                "money": raw_data[i][6]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 宣传页面
@server.route("/getCourseForMain", methods=["GET"])
def getCourseForMain():
    try:
        cursor = db.cursor()
        number = cursor.execute(
            'SELECT courseID,courseName,courseContent,startTime,endTime,coursePlace,free FROM course WHERE courseState="%s"' % "schedule")
        raw_data = cursor.fetchall()
        _data = []
        for i in range(number):
            _data.append({
                "courseID": raw_data[i][0],
                "courseName": raw_data[i][1],
                "courseContent": raw_data[i][2],
                "startTime": raw_data[i][3],
                "endTime": raw_data[i][4],
                "coursePlace": raw_data[i][5],
                "free": raw_data[i][6]
            })
        dic = {
            "status": 0,
            "msg": "",
            "data": {
                "data": _data
            }
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


# 接收公司培训申请
@server.route("/receiveCompanyApply", methods=["POST"])
def receiveCompanyApply():
    post_data = json.loads(request.get_data(as_text=True))
    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO companyapply (companyName,field,email,applyTime) VALUES'
                       ' ("%s","%s","%s","%s")' %
                       (post_data['companyName'],
                        post_data['field'],
                        post_data['companyEmail'],
                        datetime.utcfromtimestamp(int(time.time()))))
        db.commit()
        dic = {
            "status": 0,
            "msg": "添加成功！",
            "data": {}
        }
    except Exception as e:
        dic = {
            "status": 1,
            "msg": str(e),
            "data": {}
        }
    return dic


@server.route("/nothing", methods=["GET"])
def nothing():
    dic = {
        "status": 0,
        "msg": "",
        "data": {}
    }
    return dic


server.run(debug=True, port=5000)
