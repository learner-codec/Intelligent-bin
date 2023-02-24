from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt
import pymysql
import serial
import time
import binascii
import re
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys,os
sys.path.append(os.path.join(os.getcwd(),'python/'))
import darknet as dn
import pdb
import cv2
import socket
from dwebsocket import *
from django.contrib import messages
from django.http import JsonResponse


#db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
#cursor = db.cursor()

#ser1 = serial.Serial('/dev/ttyACM0', 9600)

#ser2 = serial.Serial('/dev/ttyUSB0', 19200, timeout=0.5)

#ser3 = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)

@accept_websocket
def udprecv(request):
    #return render(request,'chioce.html', {"username": username})
    print("Function Starting ...")
    if request.is_websocket():
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        s.bind(("", 39169))
        data,addr = s.recvfrom(1024)
        if len(data)>0:
            messages.success(request, "数据已接受！")
            print("Data:",data)
        else:
            message = "出错！请重试。"
            return render(request, 'login.html', {"message": message})
        hex = data.hex()
        l=len(hex)
        icard=0
        for i in range(0,4):
            icard=icard*256+int(hex[l-(i+1)*2:l-i*2],16)
        scard=str(icard)
        card=scard.zfill(10)
        """
        ard = serial.Serial('/dev/ttyACM2', 9600)
        pre_card = ard.readline()
        #ard.flush()
        card=Pre_card.strip('\r\n')
        """
        print("Card",card)

        try:
            cursor1 =db.cursor()
            cursor1.execute("select username from weixin_user where card_id=%s",card)
            username = cursor1.fetchone()
            print("UserName:",username)
            if username:                
                if  username== '123456':
                    return render(request, 'repair.html', {"username": username})
                else:
                    #user(username)
                    print("Request:",request)
                    #return render(request,"welcome")
                    return render(request,'chioce.html', {"username": username})
                    #return
            else:
                messages.success(request,"非法用户！")
                return render(request, 'index.html')
        except:
            message = "该卡不存在，请重新刷卡！"
            cursor.close()
            db.close()
            return render(request, 'login.html', {"message": message})

'''
@accept_websocket
def udprecv(request):
    print("Function Starting ...")
    if request.is_websocket():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        s.bind(("", 39169))
        data,addr = s.recvfrom(1024)
        if len(data)>0:
            messages.success(request, "数据已接受！")
            print("Data:",data)
        else:
            message = "出错！请重试。"
            return "error data received"
        hex = data.hex()
        l=len(hex)
        icard=0
        for i in range(0,4):
            icard=icard*256+int(hex[l-(i+1)*2:l-i*2],16)
        scard=str(icard)
        card=scard.zfill(10)
        try:
            db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
            cursor =db.cursor(cursor=pymysql.cursors.DictCursor)
            sql = 'select * from weixin_user where card_id=%s'
            rowcount = cursor.execute(sql, [card])
            if rowcount:
                data = cursor.fetchone()
                username=data['username']
                print("User Name= ",username)
                request.websocket.send(username)
            else:
                messages.success(request,"非法用户！")
                request.websocket.send("error login")
        except:
            messages.success(request, "数据库访问出错！")
            request.websocket.send("database access error")
'''
#this is a test code
def read_card(request):
    print('this function is running')
    ser = serial.Serial('/dev/ttyACM1', 9600)
    line =""
    ser.isOpen()
    line = ser.readline()
    print('serial opened successfull')
    line = line.decode("utf-8")
    print('line is   ',line)
    line= line.rstrip("\r\n")
    length =len(line)
    arr=[]
    line1=['']
    line1[:]=line
    for l in line1:
        print(l+"\t")

    count=0
    k=0
    val = ""
    for i in range(length):
       count = count+1
       print(line1[i])
       val=val + line1[i]
       arr.insert(k, val)
       if((count % 2)==0 & length<8):
           val=""
           k=k+1
              
       elif((count % 2)==0):
           val=""
           k=k+1 

    stri = arr[:4]
    stri = stri[::-1]   
    HEX = ''.join(map(str, stri))
    dec = int(HEX,16)
    dec = str(dec)
    if(length<8):
        dec = '0'+dec
    print('the card number is: ', dec)
    if(dec):
        card = dec
        print('card number is: ', card)
    
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
    
        try:
                cursor1 =db.cursor()
                cursor1.execute("select username from weixin_user where card_id=%s",card)
                username = cursor1.fetchone()
                print("UserName:",username)
                cursor.close()
                db.close()
        except:
                message = "该卡不存在，请重新刷卡!"
                cursor.close()
                db.close()

        print("number    ",card)
        print("Card Request:",request)
        card_info = {'card_info': username}
        print('card info  ',card_info)
    return JsonResponse(card_info)



        
#test code finished

def code(request):
    if request.method == 'GET':
        return render(request, 'code.html')
def card_new(request):
    return render(request, 'card.html')
def card(request):
    card= read_card()
    if(card):
        print('card number is: ', card)
    
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
    
        try:
                cursor1 =db.cursor()
                cursor1.execute("select username from weixin_user where card_id=%s",card)
                username = cursor1.fetchone()
                print("UserName:",username)
                if username:                
                    if  username== '123456':
                        return render(request, 'repair.html', {"username": username})
                    else:
                    #user(username)
                   # print("Request:",request)
                    #return render(request,"welcome")
                        return render(request,'white_page.html', {"username": username})
                        #return
                else:
                    messages.success(request,"非法用户！")
                    return render(request, 'index.html')
        except:
                message = "该卡不存在，请重新刷卡！"
                cursor.close()
                db.close()
                return render(request, 'login.html', {"message": message})

        print("number    ",card)
        print("Card Request:",request)
        #return render(request, 'card.html')
    
    return render(request,'white_page.html',{"card": card})
class UserForm1(forms.Form):
    username = forms.CharField(label='电话号码',max_length=20)

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        x = []
        data = UserForm1(request.POST)
        if data.is_valid():
            username1 = data.cleaned_data['username']
            x1 = x.append(username1)
            try:
                sql = "select * from weixin_user where username=%s"
                username = cursor.execute(sql,[username1])
                user1 = "123456"
                if username:
                    if username1 == user1:
                        return render(request, 'repair.html',{"username":x})
                    else:
                        user(username1)
                        return render(request, 'chioce.html',{"username":x})
                else:
                    message = "电话号码不存在，请重新输入！"
                    return render(request, 'login.html',{"message": message})
            except:
                message = "电话号码不存在，请重新输入！"
                cursor.close()
                db.close()
                return render(request, 'login.html',{"message": message})
        else:
            message = "电话号码不存在，请重新输入！"
            cursor.close()
            db.close()
            return render(request, 'login.html', {"message": message})

def chioce(request,value):
        print('the choice is', value)
        value = value.split("\s") 
        return render(request, 'chioce.html', {"username":value})

def user(username1):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("INSERT INTO weixin_scan_code(openid,sid,status,time ) values('%s','%s','%s','%s')" % (username1,1,1,datetime))
    db.commit()
    db.rollback()
    cursor.close()
    db.close()

def index(request):
    return render(request,'index.html')

def logout(request):
    if request.method == 'GET':
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        cursor.execute('UPDATE weixin_scan_code SET status = 2 where sid=1')
        db.commit()
        cursor.close()
        db.close()
        return render(request, 'index.html')

def cal2():
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("SELECT volume FROM web_b1 WHERE Sno =1 ORDER BY id desc LIMIT 1")
    mental = cursor.fetchone()
    cursor.execute("SELECT volume FROM web_b1 WHERE Sno =2 ORDER BY id desc LIMIT 1")
    clothes = cursor.fetchone()
    cursor.execute("SELECT volume FROM web_b1 WHERE Sno =3 ORDER BY id desc LIMIT 1")
    book = cursor.fetchone()
    cursor.execute("SELECT volume FROM web_b1 WHERE Sno =4 ORDER BY id desc LIMIT 1")
    plastic = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return mental,clothes,book,plastic

def sendemail():
    mental, clothes, book, plastic = cal2()
    from_addr = '1114347810@qq.com'
    password = 'hkevatfhhnjqhffb '
    to_addr = 'minhui96@163.com'
    smtp_server = 'smtp.qq.com'
    msg = MIMEText('一号箱已满请安排人员回收，谢谢！', 'plain', 'utf-8')
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('回收预警')
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

def save():
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("SELECT weight FROM web_info WHERE Sno ='1'")
    mental = cursor.fetchone()
    mental1 = np.array(mental, dtype=float)
    mental2 = mental + mental1
    score = float(mental2)
    cursor.execute('UPDATE web_info SET status = 2 where sid=1 order by id desc limit 1')
    db.commit()
    cursor.close()
    db.close()

def logout1(request):
    if request.method == 'GET':
        close1()
        #close2()
        close3()
        close4()
        return render(request, 'index.html')

def throw(request):
    if request.method == 'GET':
        return render(request, 'throw.html')

def throw1(request):  
    data = [2]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser1.write(sendStr.encode('utf-8'))
    time.sleep(0.1)
    return render(request, 'choose.html')

def throw2(request):
    data = [3]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser1.write(sendStr.encode('utf-8'))
    time.sleep(0.1)
    return render(request, 'choose 2.html')

def throw3(request):
    data = [4]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser1.write(sendStr.encode('utf-8'))
    time.sleep(0.1)
    return render(request, 'choose 3.html')

def throw4(request):
    data = [5]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser1.write(sendStr.encode('utf-8'))
    time.sleep(0.1)
    return render(request, 'choose 4.html')

def cal():
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("SELECT weight FROM web_b1 WHERE Sno =1 ORDER BY id desc LIMIT 1")
    mental = cursor.fetchone()
    cursor.execute("SELECT weight FROM web_b1 WHERE Sno =2 ORDER BY id desc LIMIT 1")
    clothes = cursor.fetchone()
    cursor.execute("SELECT weight FROM web_b1 WHERE Sno =3 ORDER BY id desc LIMIT 1")
    book = cursor.fetchone()
    cursor.execute("SELECT weight FROM web_b1 WHERE Sno =4 ORDER BY id desc LIMIT 1")
    plastic = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return mental,clothes,book,plastic

def select_score():
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("select openid from weixin_scan_code where sid=1 order by id desc LIMIT 1")
    openid = cursor.fetchone()
    cursor.execute("select score from weixin_user where username=%s or openid=%s", (openid, openid))
    score2 = cursor.fetchone()
    score3 = np.array(score2, dtype=float)
    db.commit()
    cursor.close()
    db.close()
    return score3,openid

def update_score(score,openid):
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("update weixin_user set score=%s where username=%s or openid=%s", (score, openid, openid))
    db.commit()
    cursor.close()
    db.close()
def weight1(request):
    if request.method == 'GET':
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        result1 = cal()
        arr1 = np.array(result1, dtype=float)
        close1()
        time.sleep(2)
        result2 = cal()
        arr2 = np.array(result2, dtype=float)
        w1 = arr2[0] - arr1[0]
        score1 = w1 *10
        score3,openid = select_score()
        score4 = score1 + score3
        score = float(score4)
        update_score(score,openid)
        cursor.execute("select weight from web_info where Sid=1 and Sno=1")
        weight1 = cursor.fetchone()
        weight2 = np.array(weight1, dtype=float)
        weight3 = weight2 + w1
        weight = float(weight3)
        cursor.execute("update web_info set weight=%s where Sid=1 and Sno=1",weight)
        db.commit()
        cursor.close()
        db.close()
        return render(request,'score.html',{'w1':w1})

def weight2(request):
    if request.method == 'GET':
        result1 = cal()
        arr1 = np.array(result1, dtype=float)
        close2()
        time.sleep(2)
        result2 = cal()
        arr2 = np.array(result2, dtype=float)
        w2 = arr2[1] - arr1[1]
        score1 = w2 * 10
        score3, openid = select_score()
        score4 = score1 + score3
        score = float(score4)
        update_score(score, openid)
        cursor.execute("select weight from web_info where Sid=1 and Sno=2")
        weight1 = cursor.fetchone()
        weight2 = np.array(weight1, dtype=float)
        weight3 = weight2 + w2
        weight = float(weight3)
        cursor.execute("update web_info set weight=%s where Sid=1 and Sno=2", weight)
        db.commit()
        return render(request,'score.html',{'w2':w2})

def weight3(request):
    if request.method == 'GET':
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        result1 = cal()
        arr1 = np.array(result1, dtype=float)
        close3()
        time.sleep(2)
        result2 = cal()
        arr2 = np.array(result2, dtype=float)
        w3 = arr2[2] - arr1[2]
        score1 = w3 * 10
        score3, openid = select_score()
        score4 = score1 + score3
        score = float(score4)
        update_score(score, openid)
        cursor.execute("select weight from web_info where Sid=1 and Sno=3")
        weight1 = cursor.fetchone()
        weight2 = np.array(weight1, dtype=float)
        weight3 = weight2 + w3
        weight = float(weight3)
        cursor.execute("update web_info set weight=%s where Sid=1 and Sno=3", weight)
        db.commit()
        cursor.close()
        db.close()
        return render(request,'score.html',{'w3':w3})

def weight4(request):
    if request.method == 'GET':
        db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
        cursor = db.cursor()
        result1 = cal()
        arr1 = np.array(result1, dtype=float)
        close4()
        time.sleep(2)
        result2 = cal()
        arr2 = np.array(result2, dtype=float)
        w4 = arr2[3] - arr1[3]
        score1 = w4 * 10
        score3, openid = select_score()
        score4 = score1 + score3
        score = float(score4)
        update_score(score, openid)
        cursor.execute("select weight from web_info where Sid=1 and Sno=4")
        weight1 = cursor.fetchone()
        weight2 = np.array(weight1, dtype=float)
        weight3 = weight2 + w4
        weight = float(weight3)
        cursor.execute("update web_info set weight=%s where Sid=1 and Sno=4", weight)
        db.commit()
        cursor.close()
        db.close()
        return render(request,'score.html',{'w4':w4})

def score(request):
    return render(request, 'score.html')

def recycle(request):
    return render(request,'recycle.html')

def recycle1(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 01 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser2.close()
        return render(request, 'recycle.html')

def recycle2(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 02 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser.close()
        return render(request, 'recycle.html')

def recycle3(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 05 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser2.close()
        return render(request, 'recycle.html')

def recycle4(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 06 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser2.close()
        return render(request, 'recycle.html')

def recycle5(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 04 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser2.close()
        return render(request, 'recycle.html')

def repair(request):
    while True:
        data = bytes.fromhex('A5 5A 00 00 01 A0 00 01 01 00 03 AB CD')
        ser2.write(data)
        n = ser2.inWaiting()
        if n:
            data = str(binascii.b2a_hex(ser2.read(n)))[2:-1]
            print(data)
        time.sleep(1)
        #ser2.close()
        return render(request, 'repair.html')

def recognition():
    dn.set_gpu(0)
    net = dn.load_net(b"cfg/yolov3.cfg",b"yolov3.weights",0)
    meta = dn.load_meta(b"cfg/coco.data")
    items_list = ['suitcase','fock','spoon','tie','book','keyboard','umberlla','bottle','handbag','teddybear']
    cap = cv2.VideoCapture(0)
    old_time = time.time()
    while 1:
        new_time = time.time()
        ret,frame = cap.read()
        #if count%fps == 0:
        if abs(int(new_time-old_time))==2:
            old_time = time.time()
            cv2.imwrite("data/test.jpg",frame)
            time.sleep(0.1)
            r = dn.detect(net,meta,b"data/test.jpg")
            for i in range(len(r)):
                a=r[i][0]
                b=str(a, encoding='utf-8')
                print(b)
                if b in items_list:
                    c=a
            return c

def opendoor(request):
    if request.method == 'GET':
        d=recognition()
        a=str(d, encoding='utf-8')
        print(a)        
        if a == 'book':
            throw3()
            return render(request, 'book.html')
        elif a == 'suitcase':
            throw4()
            return render(request, 'suitcase.html')
        elif a == 'fork':
            throw1()
            return render(request, 'fork.html')
        elif a == 'spoon':
            throw1()
            return render(request, 'spoon.html')
        elif a == 'tie':
            throw2()
            return render(request, 'tie.html')
        elif a == 'teddybear':
            throw2()
            return render(request, 'teddybear.html')
        elif a == 'handbag':
            throw2()
            return render(request, 'handbag.html')
        elif a == 'keyboard':
            throw4()
            return render(request, 'keyboard.html')
        elif a == 'umberlla':
            throw4()
            return render(request, 'umberlla.html')

def selectuser():
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    cursor.execute("select openid from weixin_scan_code ORDER BY id desc LIMIT 1")
    openid = cursor.fetchone()
    cursor.execute("select username from weixin_user where openid=%s or username=%s",(openid,openid))
    username = cursor.fetchone()
    cursor.close()
    db.close()
    return username

def close1():
    count = 4
    total_w = 0
    count_num_w = 0
    total_u = 0
    count_num_u = 0
    ser3 = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)
    data = [1]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser3.write(sendStr.encode('utf-8'))
    time.sleep(1)
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    b = selectuser()
    username="".join(tuple(b))
    for num in range(count):
        string = ser3.readline().decode('utf_8')
        string = str(string)
        if "w" in string:
            data_1 = re.findall(r'\d+.\d+', string)
            if len(data_1) != 0:
                data_1 = float(data_1[0])
                total_w = total_w + data_1
                count_num_w = count_num_w + 1
        else:
            data_2 = re.findall(r'\d+.\d+', string)
            if len(data_2) != 0:
                data_2 = float(data_2[0])
                total_u = total_u + data_2
                count_num_u = count_num_u + 1
    value_1 = total_w / count_num_w
    value_2 = total_u/count_num_u
    cursor.execute("INSERT INTO web_b1(Sid,Sno,weight,volume,time,user) values('%s','%s','%f','%f','%s','%s')" % (1,1,value_1,value_2,datetime,username))
    db.commit()
    cursor.close()
    db.close()
    #ser3.close()

def close2():
    count = 4
    total_w = 0
    count_num_w = 0
    total_u = 0
    count_num_u = 0
    ser3 = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)
    data = [2]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser3.write(sendStr.encode('utf-8'))
    time.sleep(1)
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    b = selectuser()
    username="".join(tuple(b))
    for num in range(count):
        string = ser3.readline().decode('utf_8')
        string = str(string)
        if "w" in string:
            data_1 = re.findall(r'\d+.\d+', string)
            if len(data_1) != 0:
                data_1 = float(data_1[0])
                total_w = total_w + data_1
                count_num_w = count_num_w + 1
        else:
            data_2 = re.findall(r'\d+.\d+', string)
            if len(data_2) != 0:
                data_2 = float(data_2[0])
                total_u = total_u + data_2
                count_num_u = count_num_u + 1
    value_1 = total_w / count_num_w
    value_2 = total_u/count_num_u
    cursor.execute("INSERT INTO web_b1(Sid,Sno,weight,volume,time,user) values('%s','%s','%f','%f','%s','%s')" % (1, 2, value_1, value_2, datetime,username))
    db.commit()
    cursor.close()
    db.close()
    #ser3.close()

def close3():
    count = 4
    total_w = 0
    count_num_w = 0
    total_u = 0
    count_num_u = 0
    ser3 = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)
    data = [3]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser3.write(sendStr.encode('utf-8'))
    time.sleep(1)
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    b = selectuser()
    username="".join(tuple(b))
    for num in range(count):
        string = ser3.readline().decode('utf_8')
        string = str(string)
        if "w" in string:
            data_1 = re.findall(r'\d+.\d+', string)
            if len(data_1) != 0:
                data_1 = float(data_1[0])
                total_w = total_w + data_1
                count_num_w = count_num_w + 1
        else:
            data_2 = re.findall(r'\d+.\d+', string)
            if len(data_2) != 0:
                data_2 = float(data_2[0])
                total_u = total_u + data_2
                count_num_u = count_num_u + 1
    value_1 = total_w / count_num_w
    value_2 = total_u/count_num_u
    cursor.execute("INSERT INTO web_b1(Sid,Sno,weight,volume,time,user) values('%s','%s','%f','%f','%s','%s')" % (1, 3, value_1, value_2, datetime,username))
    db.commit()
    cursor.close()
    db.close()
    #ser3.close()

def close4():
    count = 4
    total_w = 0
    count_num_w = 0
    total_u = 0
    count_num_u = 0
    ser3 = serial.Serial('/dev/ttyACM1', 9600, timeout=0.5)
    data = [4]
    valList = [str(x) for x in data]
    sendStr = ','.join(valList)
    ser3.write(sendStr.encode('utf-8'))
    time.sleep(1)
    db = pymysql.connect('39.96.58.232', 'root', 'af1234!', 'wxshop')
    cursor = db.cursor()
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    b = selectuser()
    username="".join(tuple(b))
    for num in range(count):
        string = ser3.readline().decode('utf_8')
        string = str(string)
        if "w" in string:
            data_1 = re.findall(r'\d+.\d+', string)
            if len(data_1) != 0:
                data_1 = float(data_1[0])
                total_w = total_w + data_1
                count_num_w = count_num_w + 1
        else:
            data_2 = re.findall(r'\d+.\d+', string)
            if len(data_2) != 0:
                data_2 = float(data_2[0])
                total_u = total_u + data_2
                count_num_u = count_num_u + 1
    value_1 = total_w / count_num_w
    value_2 = total_u/count_num_u
    cursor.execute("INSERT INTO web_b1(Sid,Sno,weight,volume,time,user) values('%s','%s','%f','%f','%s','%s')" % (1, 4, value_1, value_2, datetime,username))
    db.commit()
    cursor.close()
    db.close()
    #ser3.close()

'''
Designed and developed in HuaiYin Gong Xue Yuan - Robotics Research Lab
由淮阴工学院机器人实验室设计和开发
'''


