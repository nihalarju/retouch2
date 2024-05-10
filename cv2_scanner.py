

#Importing Libraries
import cv2
import numpy as np

# Loading an image and setting the frame size for the scanned documents
img = cv2.imread("docs.jpg")
frameWidth = 480
frameHeight = 640
cv2.imshow("Original",img)

#Processing the image
def imageProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    return imgCanny


#Getting the boundaries of the document
def GetContour(img):
    biggest = np.array([])
    bArea = 0
    contours,heirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5500 :
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02 * peri, True)
            if area > bArea and len(approx) == 4:
                biggest = approx
                bArea = area
    return biggest

#Getting the points around the boundaries
def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,2,),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis = 1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


#Warping the document
def getWarp(img,biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (frameWidth, frameHeight))
    return imgOutput

#Using the functions to get the scanned document
img = cv2.resize(img,(frameWidth,frameHeight))
result = imageProcessing(img)
biggest = GetContour(result)
imgWrapped = getWarp(img, biggest)
cv2.imshow("Output",imgWrapped)


cv2.waitKey(0)