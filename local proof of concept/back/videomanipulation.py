### in this file functions for the manipulation of non- live videos will be defined


import numpy as py
import cv2 as cv
from basicpicturemanipulation import gray_filter





path = "C:/Users/Valentin/Documents/Teamprojekt/Image-Augmentation/Image-AugmentationTP/local proof of concept/data/input/test_vid.mp4"
filename = 'C:/Users/Valentin/Documents/Teamprojekt/Image-Augmentation/Image-AugmentationTP/local proof of concept/data/output/test_vid.avi'


#this is a testing function for us if we are honest 
def show_video(video_path):

    video = cv.VideoCapture(video_path)
    while video.isOpened():
        ret, frame = video.read()
        cv.imshow('Test', frame)

        if not ret:
            print("show's over")
            break



        if cv.waitKey(20) & 0xFF==ord('d'):
            break
    video.release()
    cv.destroyAllWindows()


# this function takes a path and a filter and applies it to the video in the path, then saves the video as an .mp4 
def filter_video(video_path,apply ):
    source = cv.VideoCapture(video_path)

    #Defining codec
    fourcc = cv.VideoWriter_fourcc(* 'WMV1')
    output = cv.VideoWriter(filename, fourcc, 24.0, (852,  480))

    while source.isOpened():
        ret, frame = source.read()
      
        if not ret:
            print("Can't receive frame ( video has ended?). Exiting..")
            break
        frame = cv.resize(frame, (852,480))
        #frame = apply(frame)

        #actual writing
        output.write(frame)

        cv.imshow('frame',frame)
        if cv.waitKey(1)== ord("d"):
            break
    source.release()
    output.release()
cv.destroyAllWindows()



def grayscale_video(video_path):
    source = cv.VideoCapture(video_path)

    #Defining codec
    fourcc = cv.VideoWriter_fourcc(* 'WMV1') 
    output = cv.VideoWriter(filename, fourcc, 24.0, (852,  480),)

    while source.isOpened():
        ret, frame = source.read()
      
        if not ret:
            print("Can't receive frame ( video has ended?). Exiting..")
            break
        frame = cv.resize(frame, (852,480))
        frame = gray_filter(frame)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
        #actual writing
        output.write(frame)

        cv.imshow('frame',frame)
        if cv.waitKey(1)== ord("d"):
            break
    source.release()
    output.release()
cv.destroyAllWindows()


#filter_video(path, gray_filter)

grayscale_video(path)


    