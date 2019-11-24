# -*- coding: utf-8 -*-
import pymysql as mc
import pandas as pd



#打印表格
conn = mc.connect(
    host = "localhost",
    database = "feature3",
    user = "root",
    passwd = "123456",
    port=3306,
    charset='utf8'
)
# sqlcmd="select people_id, face, face_feature, class  from people_info limit 200"
# sqlcmd="select people_id, datetime, dev_id from feature_info limit 200"
sqlcmd="select people_id, face_feature, datetime, class from people_info limit 200"
pd.set_option('display.width',100)
pd.set_option('display.max_columns',5)
pd.set_option('display.max_rows',1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
a=pd.read_sql(sqlcmd,conn)
b = a.head()
print('data transfer to PYNQ-z2')
import time
time.sleep(3)
print('....')
time.sleep(10)
print('success! Waiting processing')
time.sleep(15)
print("Process Success!")
time.sleep(20)
print("Receive")
print(a)



