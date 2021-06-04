import cv2
import csv
import matplotlib.pyplot
import time
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os


writeout = input("What would you like your output CSV file to be called? Please do not include .csv   ")
csv_name = writeout + '.csv'
# outfile = open(csv_name, 'w')
with open(csv_name, 'w+', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    path = askdirectory(title='Select Folder') # shows dialog box and return the path
    files = os.listdir(path)
    files.sort()
    background = None
    print("Counting...")
    for f in files:
        print(f)
        if f == "background.jpg":
            filename = path + "/" + f
            background = cv2.imread(filename)
            continue
         
        # so 'junk' files don't cause the code to exit
        if f[0] == '.':
            continue
        filename = path + "/" + f
       
        # Read BGR image
        img = cv2.imread(filename)
      
        original = img.copy()
 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_bk = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
     
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh_bk = cv2.threshold(gray_bk, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    

        no_bk = cv2.subtract(thresh, thresh_bk)
        


        

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
        #Finding the contours in the image 
        contours, hierarchy = cv2.findContours(no_bk,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        sum_contours = 0
        for c in contours:
            # Obtain bounding rectangle to get measurements
            x,y,w,h = cv2.boundingRect(c)

            # Find centroid
            area = cv2.contourArea(c)
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
   
