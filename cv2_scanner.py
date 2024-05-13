

#Importing Libraries
import cv2
import numpy as np
import glob
import os

# Loading an image and setting the frame size for the scanned documents
sourcedir = r"/Volumes/termez/0_photographs/"
targetdir = r"/Volumes/termez/1_scaled/"

frameWidth = 1800
frameHeight = 1200
# cv2.imshow("Original",img)

#Processing the image
def imageProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    # imgCanny = cv2.Canny(imgBlur,5,5)
    _,threshold = cv2.threshold(imgBlur, 128, 255, cv2.THRESH_BINARY)
    return threshold


#Getting the boundaries of the document
def GetContour(img):
    biggest = np.array([])
    bArea = 0
    contours,heirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 550 :
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02 * peri, True)
            if area > bArea and len(approx) == 4:
                biggest = approx
                bArea = area
    assert len(biggest) == 4
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


# img = cv2.imread(r"/Volumes/termez/DocumentsMac/intel/1280 process front end handbook/0_photographs/IMG_7399.jpeg")
# #Using the functions to get the scanned document
# img = cv2.resize(img,(frameWidth,frameHeight))
# result = imageProcessing(img)
# biggest = GetContour(result)
# imgWrapped = getWarp(img, biggest)
# cv2.imshow("Output",imgWrapped)
# cv2.waitKey(0)


img_paths = glob.glob(sourcedir + "*.jpeg")
fail_count = 0
margin = 100

for img_path in img_paths:
    try:
        img = cv2.imread(img_path)
        img = cv2.resize(img,(frameWidth,frameHeight))
        # img = img[margin:-int(3*margin), margin:-3*margin]
        imgCanny = imageProcessing(img)
        biggest = GetContour(imgCanny)
        imgWrapped = getWarp(img, biggest)
        basename = os.path.splitext(os.path.basename(img_path))[0]
        img_target_path = os.path.join(targetdir, basename + '.png' )
        # print(img_path, img_target_path)
        cv2.imwrite(img_target_path, imgWrapped)
    except AssertionError:
        fail_count += 1
        # print(img_path)
        # print("biggest: ", biggest)
        cv2.imshow("Input",imgCanny)
        cv2.waitKey(0)
        break 
        # pass
    
print("failed images: ", fail_count)
