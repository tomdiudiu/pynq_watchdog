# -*- coding: utf-8 -*-
import cv2
import time


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

sample_rate = 10
current_frame = 0
pic_save_num = 0
file_name = "G:/Temp_Pic/"
while True:
    ret, frame = cap.read()

    current_frame += 1
    if current_frame % sample_rate == 0:
        pic_save_num += 1
        cv2.imwrite(file_name+str(pic_save_num)+".jpg",frame)

    cv2.namedWindow("Camera", 0)
    cv2.resizeWindow("Camera",800,600)
    cv2.imshow("Camera", frame)

    print(time.time())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()