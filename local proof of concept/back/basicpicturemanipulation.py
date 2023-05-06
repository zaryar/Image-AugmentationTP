#basic functions for the manipulation of pictures are done here

import cv2 as cv
import numpy as np
import os 


test = "Test.jpeg"
def get_path(folder, image):
    #gets the path to the image and hopefully working on *nix and Windows
    #folder is the name of the folder in data the image is saved in
    #image is the name of the image

    #getting the current directory
    cur_dir = os.getcwd()
    #going up a directory
    os.chdir("..") 
    #constucting the path 
    path = os.path.join(os.getcwd(),'data',folder, image)

    #going back to the original directory
    os.chdir(cur_dir)
   
    return path


def read_picture():
        #getting the right path for the machine
        path = get_path("input", test)

       

        img = cv.imread(path)

        return img

def gray_filter(img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        return gray

def show_image(img, gray):
        cv.imshow('Original image',img)
        cv.imshow('Gray image', gray)

        cv.waitKey(0)
        cv.destroyAllWindows()

def write_image(gray):
        cv.imwrite(get_path("output",test), gray)