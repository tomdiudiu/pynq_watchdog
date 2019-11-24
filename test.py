import cv2
cap=cv2.VideoCapture("https://192.168.137.10:8081/")
while True:
    success,img=cap.read()
    cv2.imshow("camera",img)