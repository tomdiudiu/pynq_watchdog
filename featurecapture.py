# import mysql.connector as mc
import pymysql as mc
import numpy as np
import cv2
import dlib
import os
import time
import warnings
import pandas as pd
import random

# 获取当前路径
# current_path = os.getcwd()
current_path = ''
# 获取模型路径
predictor_path = current_path + "./model/shape_predictor_68_face_landmarks.dat"
face_rec_model_path = current_path + "./model/dlib_face_recognition_resnet_model_v1.dat"
# 获取测试图片路径
faces_folder_path = current_path + "C:/Users/tomdiudiu/Desktop/pic/"
# 读入模型
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

# 获取特征类
class capture_feature:
# 定义构造方法
    def __init__(self):
        self.init_data()
        self.init_database()

# 定义基本方法
    # 初始化数据
    def init_data(self):
        self.av_frame_rate = 25
        self.face_cap_period =300  # 设置人脸采集时间间隔（单位：ms）
        self.fea_cap_period = 30  # 设置特征（时间、设备号）采集时间间隔（单位：s）

        self.list_face_feature = []  # 该列表加载数据库中people_info表中的face_feature
        self.current_face_feature = np.zeros((128,), dtype = float)  # 存放当前人脸的128维特征向量

        self.list_peo_peo_id = []  # 该列表加载数据库中people_info表中的people_id
        self.list_fea_peo_id = []  # 该列表加载数据库中feature_info表中的people_id
        self.list_class_id = []
        self.class_id = 1
        self.current_peo_id = 1  # 存放当前人脸的people_id

        self.list_datetime = []  # 该列表加载数据库中feature_info表中的datetime
        self.current_datetime = ''  # 存放当前datetime

        self.dev = 0  # 设备选择，0代表默认摄像设备
        self.dev_id = 123456789  # 设备编号，与地理位置绑定

        self.img_path_name = ''  # 截取人脸照片存放路径

        self.last_datetime = ""
        self.peo_class = ""

        self.list_class = []

        self.list_last_datetime = []

        self.list_dev_id = []
 
    # 初始化mysql数据库   
    def init_database(self):
        db = mc.connect(  # 连接本地数据库管理系统
            host = 'localhost',
            user = 'root',
            passwd = '123456')
        
        cur = db.cursor()  # 获取游标
        cur.execute('create database if not exists feature3')  # 创建一个名为feature的数据库（若feature不存在）
        cur.execute('use feature3')  # 选择feature数据库
        cur.execute("""create table if not exists fig_info  
        (people_id int auto_increment primary key,
        face mediumblob not null,
        face_feature blob
        )""")  # 创建表格fig_info
        cur.execute("""create table if not exists feature_info
        (people_id int not null,
        datetime text not null,
        dev_id int not null
        )""")  # 创建表格feature_info
        cur.execute("""create table if not exists people_info
        (people_id int not null,
        face_feature blob,
        datetime text not null,
        class int
        )""")  # 创建表格people_info


        cur.close()  # 关闭游标
        db.commit()  # 提交修改
        db.close()  # 关闭与数据库管理系统的连接

    # 将数据写入数据库
    def insert_data(self,types):
        db = mc.connect(host = 'localhost',user = 'root',passwd = '123456',database = 'feature3')
        cur = db.cursor()

        # 写入people_info表格数据
        if types == 1:
            # 从指定路径读取照片
            fp = open(self.img_path_name,'rb')
            img = fp.read()
            fp.close()
            #print(type(img),'\n',img)  #【测试】
        
            # 将数组转化为字符串
            numpy_bytes = self.current_face_feature.tostring()  

            sql = "insert into fig_info (face,face_feature) values (%s,%s)"
            val = (img,numpy_bytes)
            cur.execute(sql,val)

        # 写入feature_info表格数据
        if types == 2:
            sql = "insert into feature_info (people_id,datetime,dev_id) values (%s,%s,%s)"
            val = (self.current_peo_id,self.current_datetime,self.dev_id)
            cur.execute(sql,val)

        # 写入people_info表格数据
        if types == 3:
            # 将数组转化为字符串
            numpy_bytes = self.current_face_feature.tostring()

            sql = "insert into people_info (people_id,face_feature,datetime,class) values (%s,%s,%s,%s)"
            val = (self.class_id, numpy_bytes,self.last_datetime,self.peo_class)
            cur.execute(sql, val)

        cur.close()
        db.commit()
        db.close()

    # 加载数据库中特征信息
    def load_feature(self,types):
        db = mc.connect(host = 'localhost',user = 'root',passwd = '123456',database = 'feature3')
        cur = db.cursor()

        # 加载fig_info表中people_id和face_feature
        if types == 1:
            sql = 'select people_id,face_feature from fig_info'
            cur.execute(sql)
            res = cur.fetchall()
            #print('res',type(res))  

            if res != None:
                for row in res:
                    #print('row',type(row))  
                    #print(row)
                    self.list_peo_peo_id.append(row[0])  # 加载people_id
                    numArr = np.fromstring(string=row[1], dtype=float)  
                    numArr.shape = (128,)
                    self.list_face_feature.append(numArr)  # 加载face_feature
                #print(self.list_face_feature)

        # 加载feature_info表中people_id、datetime,dev_id
        if types == 2:
            sql = 'select people_id,datetime,dev_id from feature_info'
            cur.execute(sql)
            res = cur.fetchall()
  
            if res != None:
                for row in res:
                    self.list_fea_peo_id.append(row[0])
                    self.list_datetime.append(row[1])
                    self.list_dev_id.append(row[2])

        # 加载people_info表中people_id,face_feature,datetime,class
        if types == 3:
            sql = 'select people_id,face_feature,datetime,class from people_info'
            cur.execute(sql)
            res = cur.fetchall()

            if res != None:
                for row in res:
                    self.list_class_id.append(row[0])  # 加载people_id
                    numArr = np.fromstring(string=row[1], dtype=float)
                    numArr.shape = (128,)
                    self.list_face_feature.append(numArr)  # 加载face_feature
                    self.list_last_datetime.append(row[2])
                    self.list_class.append(row[3])

                #print(self.list_face_feature)


        cur.close()
        db.close()

    # 将数据库中照片读取到指定路径
    def read_picture(self,path,people_id):
        db = mc.connect(host = 'localhost',user = 'root',passwd = '123456',database = 'feature3')
        cur = db.cursor()

        # 从mysql数据库读取照片
        sql = "select face from fig_info where people_id= %s" % (people_id+1)
        cur.execute(sql)
        img = cur.fetchone()

        # 将照片保存到指定路径
        fp = open(path,'wb')
        fp.write(img[0])
        fp.close()

        # 窗口显示照片
        # img = cv2.imread(path,1)
        # cv2.imshow('people',img)
        # cv2.waitKey(0)

        cur.close()
        db.close()

    # 获取当前时间
    def getDateAndTime(self):
        dateandtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #return "["+dateandtime+"]"
        return dateandtime

    # 将时间字符串（y-m-d h:m:s）转化为时间戳
    def time_str_2_stamp(self,time_str): 
        # 先转换为时间数组
        timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        #print(timeArray)
 
        # 转换为时间戳
        timeStamp = int(time.mktime(timeArray))
        #print(timeStamp)
        return timeStamp


    # 输入两个人脸特征数组，返回欧氏距离判断结果
    def return_euclidean_distance(self,feature_1, feature_2):

        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        print("欧式距离: ", dist)
        if dist > 0.5:
            return False
        else:
            return True


    # 截取人脸图片
    def face_capture(self):
        num = 1  # 保存num张人脸照片
        self.load_feature(1)  # 加载people_info表数据
        self.load_feature(2)  # 加载feature_info表数据
        self.load_feature(3)

        cap = cv2.VideoCapture('http://192.168.137.10:8081')  # 建立视频捕获对象

        countdown = int(self.face_cap_period / self.av_frame_rate)
        # print(countdown)
        countdown_point = countdown
        Flag = 1    #允许采集人脸

        while cap.isOpened():  # 判断设备是否初始化成功

            #重置倒计时指针
            if countdown_point == 0:
                Flag = 1
                countdown_point = countdown

            ret, img = cap.read()  #逐帧捕获
            if not ret:  # 若获取帧失败，则退出
                print('获取帧失败！')
                break

            dets = detector(img, 1)   # 【检测人脸】
            #print("Number of faces detected: {}".format(len(dets))) # 打印该帧检测到的人脸数
            self.current_datetime = self.getDateAndTime()  # 获取检测人脸时的日期时间

            if dets and Flag:
                for index, face in enumerate(dets):  # 【遍历检测到的人脸】
                    #获取人脸照片
                    self.img_path_name = 'capture/%d.jpg' % num
                    img_face = img[face.top():face.bottom(),face.left():face.right()]
                    #print('imageType',type(image))  # 【测试】
                    feature_68 = shape_predictor(img, face)   # 【提取68个特征点】
                    vector_128 = face_rec_model.compute_face_descriptor(img, feature_68)   # 【计算人脸的128维的向量】
                    self.current_face_feature = np.array(vector_128)  # 将向量转化为数组
                    #print(current_face_feature)  # 【测试】



                    # 将数据写入people_info表和相关本地列表
                    cv2.imwrite(self.img_path_name,img_face)  # 将当前人脸照片保存到指定路径
                    self.insert_data(1)  # 将人脸照片和人脸特征写入数据库
                    self.list_face_feature.append(self.current_face_feature)  # 将当前人脸特征加载到本地列表
                    # 将数据写入feature_info表和相关本地列表
                    if len(self.list_peo_peo_id) == 0:
                        self.current_peo_id = 1
                    else:
                        self.current_peo_id = self.list_peo_peo_id[-1]+1
                    self.list_peo_peo_id.append(self.current_peo_id)  # 将当前人脸id加载到本地列表
                    self.insert_data(2)  # 将当前人脸id、日期时间和设备编号写入数据库
                    self.list_datetime.append(self.current_datetime)  # 将当前时间保存到本地列表
                    self.list_fea_peo_id.append(self.current_peo_id)  # 将当前人脸id保存到本地列表
                        # num += 1  # 保存照片数加1


                    ##查找对象类别
                    for i in range(len(self.list_class_id)):
                        if self.return_euclidean_distance(self.list_face_feature[i],self.current_face_feature):
                            if self.list_class_id[i] == 0:
                                print("访客"+"     "+"上次出现时间："+self.list_last_datetime[i])
                                break
                            else:
                                print("住户"+"     "+"上次出现时间："+self.list_last_datetime[i])
                                break
                        else:
                            print("未记录对象")
                            break


                    # 在图像上框出人脸并显示
                    cv2.rectangle(img,(face.left(),face.top()),(face.right(),face.bottom()),(0,0,255),2)
                    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)  #创建窗口
                    cv2.imshow('frame',img)  #显示照片
                    num += 1
                    Flag = 0

                    #显示更新数据库
                    db = mc.connect(host='localhost', user='root', passwd='123456', database='feature3')
                    sqlcmd="select people_id, datetime, dev_id from feature_info limit 2000"
                    sqlcmd2 = "select people_id, face, face_feature from fig_info limit 2000"
                    pd.set_option('display.width', 100)
                    pd.set_option('display.max_columns', 5)
                    pd.set_option('display.max_rows', 1000)
                    pd.set_option('display.unicode.ambiguous_as_wide', True)
                    pd.set_option('display.unicode.east_asian_width', True)
                    a = pd.read_sql(sqlcmd, db)
                    b = pd.read_sql(sqlcmd2,db)
                    # print(b)
                    # print(a)




            else:
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)  # 创建窗口
                cv2.imshow('frame', img)  # 显示照片

            countdown_point -= 1



            # 按‘q’退出 
            k = cv2.waitKey(self.av_frame_rate) #设置人脸采集时间间隔
            if k == ord('q'):
                cv2.destroyAllWindows()
                break

warnings.filterwarnings("ignore")
task1 = capture_feature()
task1.face_capture()
# task1.load_feature(1)
# print(task1.list_peo_peo_id)
# for i in range(len(task1.list_peo_peo_id)):
#     task1.read_picture("./capture/pic"+str(i)+'.jpg',task1.list_peo_peo_id[i])



    
