import cv2
import numpy as np

###Face Detection###
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
img = cv2.imread('man.jpg')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w,y+h), (120, 120, 0), 2)


cv2.imshow("Result", img)
cv2.waitKey(0)


###Contour/Shape Detection###
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            print(approx)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            

            if objCor == 3: ObjectType = "Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    ObjectType='Square'
                else:
                    ObjectType = 'Rect'
            elif objCor>100:
                ObjectType='Circle'
            else: ObjectType='None'
            cv2.rectangle(imgContour, (x-20, y-20), (x+w+20, y+h+20), (120, 120, 0), 2)
            cv2.putText(imgContour, ObjectType,
                        (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (120, 225, 0))



img = cv2.imread('Vector-Logo-Shapes.jpg')
img = cv2.resize(img, (640, 480))
imgContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

get_contours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.6, ([img, imgGray, imgBlur],
                             [imgCanny, imgContour, imgBlank]))

cv2.imshow('Original', imgStack)
cv2.waitKey(0)



###Color Detection###

"""def empty(a):
   pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",0,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",31,255,empty)
cv2.createTrackbar("Val Min","TrackBars",70,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)
 
while True:
    img = cv2.imread('lotus.jpg')
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
 
 
#    cv2.imshow("Original",img)
#    cv2.imshow("HSV",imgHSV)
#    cv2.imshow("Mask", mask)
#    cv2.imshow("Result", imgResult)

#    cv2.waitKey(1)

###Joining Images###

#img = cv2.imread('man.jpg')

#imgHor = np.hstack((img, img))
#imgVer = np.vstack((img, img))

#imgBlur = cv2.GaussianBlur(imgHor, (7,7), 0)

#cv2.imshow("Hroizontal", imgHor)
#cv2.imshow("Vertcal", imgVer)
#cv2.imshow("Blur", imgBlur)

###Warp Perspective###

#img = cv2.imread('cards.jpg')


#cv2.imshow('cards', img)


#width, height = 250, 350
pts1 = np.float32([[254, 109], [550, 67], [317, 587], [622, 544]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))

#cv2.imshow('Image', img)
#cv2.imshow('Warp', imgOutput)"""



###Shapes###

#img = np.zeros((512, 512, 3), np.uint8)
#img[200:400, 100:200] = 120, 135, 20

#cv2.line(img, (0, 0), (250, 325), (125, 200, 10), 3)
#cv2.rectangle(img, (150, 150), (300, 250), (125, 200, 10), cv2.FILLED)
#cv2.circle(img, (200, 200), 30, (255, 200, 0), cv2.FILLED)
#cv2.putText(img, "Opencv", (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 1)

#cv2.imshow('IMAGE', img)
###Cropping###

#img = cv2.imread('Cool.jpg')
#imgRezize = cv2.resize(img, (200, 300))
#imgCropped = img[0:300, 200:420]

###Styling###

#kernel = np.ones((5,5), np.uint8)

#imgGray = cv2cvtColor(img, cv2.COLOR_BGR2GRAY)
#imgBlur = cv2.GaussianBlur(img, (7,7), 0)
#imgCanny = cv2.Canny(img, 500, 300)
#imgDialation = cv2.dilate(imgCanny, kernel, iterations=2)

#cv2.imshow('Gray', imgGray)
#cv2.imshow('Blur', imgBlur)
#cv2.imshow('Canny', imgCanny)
#cv2.imshow('Dialation', imgDialation)
#cv2.imshow('IMage', img)
#cv2.imshow('Resize', imgRezize)
#cv2.imshow('Cropped', imgCropped)


   
