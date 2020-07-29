##import Libraries
import cv2
import time
import numpy as np

##reading through the webcam
cap = cv2.VideoCapture(0)

##Set the frame size same as the output generated
cap.set(3,640)
cap.set(4,480)

##Preperation for writing output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

## Allow the system to sleep for 3 seconds before the webcam starts
time.sleep(3)
count = 0
background = 0

## Capture the background in range of 60 for every frame
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

## Read every frame from the webcam, until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, axis=1)

    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Generate masks to detect red color (this can be changed too)
    
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([100, 40, 40])        
    upper_red = np.array([100, 255, 255]) 
    mask1 = cv2.inRange(hsv, lower_red, upper_red) 
    # setting the lower and upper range for mask2  
    lower_red = np.array([155, 40, 40]) 
    upper_red = np.array([180, 255, 255]) 
    mask2 = cv2.inRange(hsv, lower_red, upper_red) 


    #summing up the masks
    mask1 = mask1 + mask2 
  
    # Refining the mask corresponding to the detected red color 
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), 
                                         np.uint8), iterations = 2) 
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1) 
    mask2 = cv2.bitwise_not(mask1) 
  
    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask = mask1) 
    res2 = cv2.bitwise_and(img, img, mask = mask2) 
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
  
    cv2.imshow("INVISIBLE MAN", final_output) 
    k = cv2.waitKey(1) 
    if k == 27:     #break when escape key is pressed
        break


cap.release()
cv2.destroyAllWindows()

