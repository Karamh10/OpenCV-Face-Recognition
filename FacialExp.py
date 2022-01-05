#Karam Hallak
#this program detects the users face and their facial expressions
#it prints blink when they blink
#it prints mouth open/closed when it's open or closd
#it prints yes for a headnod and no when they shake thier head


######### PRESS ESC TO EXIT #################



#import
import cv2
import dlib
import math
from imutils import face_utils
import imutils 
import numpy as np

#global variables
BLINK_RATIO_THRESHOLD = 5.7
thresholdX = 100/68
thresholdY = 100/68
frameNum = -1
arrayX = []
arrayY = []

#functions to calculate midpoint
def midwayPoint(point1 ,point2):
  return (point1.x + point2.x)/2,(point1.y + point2.y)/2

#function to calculate the distance between two points and their coordinates
def euclidean_distance(point1 , point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#functions to detect eye blinking
def isBlinking(eye_points, facial_landmarks):
  
  #loading all the required points
  left  = (facial_landmarks.part(eye_points[0]).x, 
                  facial_landmarks.part(eye_points[0]).y)
  right = (facial_landmarks.part(eye_points[3]).x, 
                  facial_landmarks.part(eye_points[3]).y)
  
  center_top    = midwayPoint(facial_landmarks.part(eye_points[1]), 
                           facial_landmarks.part(eye_points[2]))
  center_bottom = midwayPoint(facial_landmarks.part(eye_points[5]), 
                           facial_landmarks.part(eye_points[4]))

  #calculate distance 
  horizontal = euclidean_distance(left,right)
  vertical = euclidean_distance(center_top,center_bottom)

  ratio = horizontal / vertical

  return ratio

def mouth_open(lip_points, facial_landmarks):
  
  #load the points
  left  = (facial_landmarks.part(lip_points[0]).x, 
                  facial_landmarks.part(lip_points[0]).y)
  right = (facial_landmarks.part(lip_points[6]).x, 
                  facial_landmarks.part(lip_points[6]).y)
  
  center_top    = midwayPoint(facial_landmarks.part(lip_points[2]), 
                           facial_landmarks.part(lip_points[4]))
  center_bottom = midwayPoint(facial_landmarks.part(lip_points[8]), 
                           facial_landmarks.part(lip_points[10]))

  #calculating distance
  horizontal = euclidean_distance(left,right)
  vertical = euclidean_distance(center_top,center_bottom)

  ratio = vertical / horizontal

  return ratio

def head_nod(frame, lmarks, facial_landmarks):

  pointA = (facial_landmarks.part(28).x, facial_landmarks.part(28).y)
  pointB = (facial_landmarks.part(29).x, facial_landmarks.part(29).y)
  #print('point a: ' + str(pointA))
  lmarks = face_utils.shape_to_np(lmarks)
  pointX = []
  pointY = []
  sum1 = 0
  sum2 = 0

  for (x, y) in lmarks:
    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    #every 5 frames insert coordinates
    if frameNum % 3 == 0:
      pointX.append(facial_landmarks.part(28).x)
      pointY.append(facial_landmarks.part(28).y)

  #every 5 frames insert more coordinates
  if frameNum % 3 == 0:
    arrayX.append(pointX)
    arrayY.append(pointY)

  #
  if frameNum % 3 == 0 and frameNum != 0:
    x1 = arrayX[len(arrayX) - 1]
    x2 = arrayX[len(arrayX) - 2]
    y1 = arrayY[len(arrayY) - 1]
    y2 = arrayY[len(arrayY) - 2]

    for p in range (0, len(y2)):
      sum1 = sum1 + math.sqrt(abs(y1[p]*y1[p] - y2[p]*y2[p]))
      sum2 = sum2 + math.sqrt(abs(x1[p]*x1[p] - x2[p]*x2[p]))
      sum1 = sum1 / 68
      sum2 = sum2 / 68

    if sum1 > thresholdY and sum2 < thresholdX:
      
      print(' \n \n YES \n \n')
    elif sum1 < thresholdY and sum2 > thresholdX:
      print('\n \n NO \n \n')
  
  return True

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#name of the display window
cv2.namedWindow('FacialExpressions')

#detect face using dlib
detector = dlib.get_frontal_face_detector()

#detect the eyes using the shape predictor and the landmarks on the picture
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]
lip_landmarks = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

while True:
  #capturing frames
  frameNum = frameNum + 1
  retval, frame = cap.read()

  #if frame not found the error
  if not retval:
      print("Can't receive frame (stream end?). Exiting ...")
      break 

  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  #detecting face in the frame from the video
  faces,_,_ = detector.run(image = frame, upsample_num_times = 0, 
                     adjust_threshold = 0.0)

  #call the is blinking function
  for face in faces:
      
      landmarks = predictor(frame, face)

      left_eye_ratio  = isBlinking(left_eye_landmarks, landmarks)
      right_eye_ratio = isBlinking(right_eye_landmarks, landmarks)
      mouth_ratio = mouth_open(lip_landmarks, landmarks)
      head = head_nod(frame, landmarks, landmarks)
      blink_ratio = (left_eye_ratio + right_eye_ratio) / 2
      #print(str(mouth_ratio))
      if blink_ratio > BLINK_RATIO_THRESHOLD:
          #if blinking is detected
          #cv2.putText(frame,"Blink",(10,50), cv2.FONT_HERSHEY_SIMPLEX,
                      #2,(255,255,255),2,cv2.LINE_AA)
          print('\n \n Blink \n \n')
      if mouth_ratio > 0.5:
          #mouth is open so print text
          #cv2.putText(frame,"MOUTH OPEN",(10,50), cv2.FONT_HERSHEY_SIMPLEX,
                      #2,(255,255,255),2,cv2.LINE_AA)
          print('\n \n Mouth Open \n \n')
      else:
          #cv2.putText(frame,"MOUTH CLOSED",(10,50), cv2.FONT_HERSHEY_SIMPLEX,
                      #2,(255,255,255),2,cv2.LINE_AA)
          print('Mouth Closed')
  cv2.imshow('FacialExpressions', frame)
  key = cv2.waitKey(1)
  if key == 27:
      break


cap.release()
cv2.destroyAllWindows()