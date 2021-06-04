import cv2
import csv
import matplotlib.pyplot
import time
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os

#image426235955

writeout = input("What would you like your output CSV file to be called? Please do not include .csv   ")
csv_name = writeout + '.csv'
# outfile = open(csv_name, 'w')
with open(csv_name, 'w+', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    path = askdirectory(title='Select Folder') # shows dialog box and return the path
    # #print(path)  
    #path = '/Users/ananya/Desktop/apr26 cropped day'
    files = os.listdir(path)
    files.sort()
    # count = 0
    # sum = 0
    background = None
    print("Counting...")
    for f in files:
        print(f)
        if f == "background.jpg":
            filename = path + "/" + f
            background = cv2.imread(filename)
            continue
        if f[0] == '.':
            continue
        # count += 1
        filename = path + "/" + f
        # print(os.path.isfile(filename))
        # print(os.path.getsize(filename))
        # Read BGR image
        img = cv2.imread(filename)
       

        # height, width, _ = np.shape(img)
        # avg_color_per_row = np.average(img, axis=0)

        # # calculate the averages of our rows
        # avg_colors = np.average(avg_color_per_row, axis=0)

        # # so, convert that array to integers
        # int_averages = np.array(avg_colors, dtype=np.uint8)
        # print(f'int_averages: {int_averages}')

        # # create a new image of the same height/width as the original
        # average_image = np.zeros((height, width, 3), np.uint8)
        # # and fill its pixels with our average color
        # average_image[:] = int_averages

        # finally, show it side-by-side with the original
        # cv2.imshow("Avg Color", np.hstack([img, average_image]))
        original = img.copy()
        # if f == "image0000007.jpg":
        #     break
        #img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
        # Converting color from BGR to RGB
        #no_bk = cv2.subtract(img, background)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_bk = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        # if f == "image0000008.jpg":
        #      cv2.imwrite("grayscale.jpg", gray)
        # blur = cv2.GaussianBlur(gray, (3,3), 0)
        # blur_bk = cv2.GaussianBlur(gray_bk, (3,3), 0)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh_bk = cv2.threshold(gray_bk, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # if f == "image0000008.jpg":
        #      cv2.imwrite("binary_threshold.jpg", thresh)

        no_bk = cv2.subtract(thresh, thresh_bk)
        # if f == "image0000008.jpg":
        #     cv2.imwrite('subtracted.jpg', no_bk)


        # # Declaring some variables
        # MIN,LOW,HUE = 0, 0, 0
        # MAX,HIGH,SAT = 1, 1, 1
        # VAL = 2
        # # Tuple for storing HSV range
        # HSV_Range = ((0, 0, 0), (179, 255, 255))
        # # List for storing HSV values
        # HSV_Values = [[20, 170, 170], [179, 255, 255]]
        # # Storing HSV values in a scalar array
        # lower_HSV = np.array([HSV_Values[LOW][HUE],HSV_Values[LOW][SAT],HSV_Values[LOW][VAL]])
        # upper_HSV = np.array([HSV_Values[HIGH][HUE],HSV_Values[HIGH][SAT],HSV_Values[HIGH][VAL]])

        # # Converting BRG image to HSV image
        # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        # processed_img = cv2.inRange(hsv_img, lower_HSV, upper_HSV)
        # cv2.imwrite('thresh_img.jpg', processed_img)

        # Getting rid of grains and noise
        kernel_4 = np.ones((4,4),np.uint8)
        kernel_2 = np.ones((4,4),np.uint8)
        no_bk = cv2.erode(thresh, kernel_2, iterations=2)
        no_bk = cv2.dilate(no_bk, kernel_4, iterations=2)

        if f == "image427000600.jpg":
            cv2.imwrite('no_noise.jpg', no_bk)

        # edged = cv2.Canny(no_bk, 230, 250)

        # cv2.imwrite('edged.jpg', edged)

        ROI_number = 0
        contours, hierarchy = cv2.findContours(no_bk,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # print("Contour length " + str(len(contours)))
        sum_contours = 0
        for c in contours:
            # Obtain bounding rectangle to get measurements
            x,y,w,h = cv2.boundingRect(c)

            # Find centroid
            
            area = cv2.contourArea(c)
            # print(str(area))
            if (area < 3000):
                sum_contours += 1
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cX, cY = 0, 0

            # Crop and save ROI
            ROI = original[y:y+h, x:x+w]
            #cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
            ROI_number += 1

            # Draw the contour and center of the shape on the image
            cv2.rectangle(img,(x,y),(x+w,y+h),(36,255,12), 4)
            cv2.circle(img, (cX, cY), 10, (320, 159, 22), -1) 
        writer.writerow([sum_contours])
        if f == "image427000600.jpg":
            cv2.imwrite("COUNTED.png", img)
            exit(0)


            # # Processing data
            # arr = np.zeros(shape = (len(contours)))
            # for i in range(len(contours)):
        #     area = cv2.contourArea(contours[i])
        #     arr[i] = area
        #     mean_arr = np.mean(arr)
        # count = 0
        # result_img = rgb_img.copy()
        # for i in range(len(contours)):
        #     # Getting the center coordinate of the contour
        #     m = cv2.moments(contours[i])
        #     center_x = int(m["m10"]/m["m00"])
        #     center_y = int(m["m01"]/m["m00"])
        #     # Counting and displaying counted object in circle
        #     if arr[i] < 1.65*mean_arr:
        #         cv2.circle(result_img, (center_x, center_y), radius = 20, color = (0,255,0),thickness = 2)
        #         count += 1
        #     else:
        #         for j in range(2):
        #             cv2.circle(result_img,(center_x, center_y),radius = 20+10*j,color = (0,255,0),thickness = 2)
        #             count += 2
        # cv2.imwrite('circled.jpg', result_img)