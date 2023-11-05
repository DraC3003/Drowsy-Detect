import numpy as np
import dlib
from imutils import face_utils
import cv2

caputre=cv2.VideoCapture(0)

detector=dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")



sleepy=0
partial=0
awake=0
status=""
color=(0,0,0)

def dist(a,b):
    distance=np.linalg.norm(a-b)
    return distance

def eye(a,b,c,d,e,f):
    upper=dist(b,d)+dist(c,e)
    lower=dist(a,f)
    rat=upper/(2.0*lower)

    if(rat>0.25):
        return 2
    elif(rat>0.21 and rat<=0.25):
        return 1
    else:
        return 0
    

while True:
    a,frame=caputre.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=detector(gray)

    for face in faces:
        x1=face.left()
        x2=face.right()
        y1=face.top()
        y2=face.bottom()

        face_frame=frame.copy()
        cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)
        

        landmarks=predictor(gray,face)
        landmarks=face_utils.shape_to_np(landmarks)



        left_eye=eye(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
        right_eye=eye(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])

        if(left_eye==0 or right_eye==0):
            sleepy+=1
            partial=0
            awake=0
            if(sleepy>6):
                status="Sleeping"
                color=(255,0,0)
        elif(left_eye==1 or right_eye==1):

            sleepy=0
            partial+=1
            awake=0
            if(partial>6):
                status="Partial Sleeping"
                color=(255,0,0)
        else:
            sleepy=0
            partial=0
            awake+=1
            if(awake>6):
                status="awake"
                color=(255,0,0)


        cv2.putText(frame,status,(100,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)
        
        for n in range(0,68):
            (x,y)=landmarks[n]
            cv2.circle(face_frame,(x,y),1,(255,0,0),-1)\
        

        cv2.imshow("Frame",frame)
        cv2.imshow("Result",face_frame)
        key=cv2.waitKey(1)
        if key==27:
            break











