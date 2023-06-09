### in this file functions for the manipulation of non- live videos will be defined


import numpy as py
import cv2 as cv






PATH = "./local_version/data/input/test_vid.mp4"
FILENAME = './local_version/data/output/test_vid.avi'
CODEC = 'WMV1'
ASPECTPATH = "./local_version/data/input/aspect_test.mp4" #we can use that to show that the format think works

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


# this function takes a path and a filter and applies it to the video in the path, then saves the video as an .avi / only works for pictures with all color channels availabl
def filter_video(video_path,apply, filename):
    source = cv.VideoCapture(video_path)

    if source.isOpened():
        WIDTH = int( source.get(cv.CAP_PROP_FRAME_WIDTH))
        HEIGHT= int(source.get(cv.CAP_PROP_FRAME_HEIGHT))
    print(HEIGHT)
    print(WIDTH)
    #Defining codec
    fourcc = cv.VideoWriter_fourcc(* CODEC )
    output = cv.VideoWriter(filename, fourcc, 24.0, (WIDTH,  HEIGHT))

    while source.isOpened():
        ret, frame = source.read()
      
        if not ret:
            print("Can't receive frame ( video has ended?). Exiting..")
            break
  
        frame = apply(frame)

        #actual writing
        output.write(frame)

        cv.imshow('frame',frame)
        if cv.waitKey(1)== ord("d"):
            break
    source.release()
    output.release()
    cv.destroyAllWindows()