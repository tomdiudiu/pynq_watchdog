import pymysql as mc
import numpy as np
import cv2
import dlib
import os
import time
import warnings
import pandas as pd
import featurecapture
import classify

task = featurecapture.capture_feature()
task.load_feature(1)
task.load_feature(2)

print(task.list_peo_peo_id)
print(task.list_fea_peo_id)
print(task.list_face_feature)
print(task.list_datetime)
print(task.list_dev_id)

exist_list = task.list_peo_peo_id
finished_list = []
lenth = len(task.list_peo_peo_id)

for i in range(lenth):
    ii = i+1
    if ii in exist_list:
        sub_list = [ii]
        for j in range(lenth):
            jj = j+1
            if jj in exist_list and jj != ii:
                if task.return_euclidean_distance(task.list_face_feature[i],task.list_face_feature[j]):
                    exist_list.remove(jj)
                    print(exist_list)
                    sub_list.append(jj)
        exist_list.remove(ii)
        # print(exist_list)
        finished_list.append(sub_list)

print(finished_list)

datetime_io_finished_list = []
for i in range(len(finished_list)):
    sub_datetime_io_list = []
    for j in range(len(finished_list[i])):
        if task.list_dev_id[finished_list[i][j]-1] == "123456789":
            sub_datetime_io_list.append([task.list_datetime[finished_list[i][j] - 1],'in'])
        else:
            sub_datetime_io_list.append([task.list_datetime[finished_list[i][j] - 1],'out'])
    datetime_io_finished_list.append(sub_datetime_io_list)

print(datetime_io_finished_list)

numMat,daylist = classify.caculateIOandDay(datetime_io_finished_list)
numMat = np.mat(numMat)
myCentroids,clustAssing = classify.kMeans(numMat,2)
print(clustAssing)

for i in range(len(finished_list)):
    task.class_id = i+1
    task.current_face_feature = task.list_face_feature[finished_list[i][0]-1]
    task.last_datetime = datetime_io_finished_list[i][-1][0]
    task.peo_class = str(clustAssing[i,0])
    task.insert_data(3)




