### in this file functions for the manipulation of non- live videos will be defined
import numpy as py
import cv2 as cv





path = "C:/Users/Valentin/Documents/Teamprojekt/Image-Augmentation/Image-AugmentationTP/local proof of concept/data/input/test_vid.mp4"




def read_video():

    video = cv.VideoCapture(path)
    while True:
        isTrue, frame = video.read()
        cv.imshow('Test', frame)

        if cv.waitKey(20) & 0xFF==ord('d'):
            break
    video.release()
    cv.destroyAllWindows()

read_video()








    