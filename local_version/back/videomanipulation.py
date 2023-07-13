### in this file functions for the manipulation of non- live videos will be defined


import numpy as py
import cv2 as cv
import torch.nn as nn
from fast_ns.experiments.filters_for_images import video_preprocessing,video_reprocessing





PATH = "./local_version/data/input/test_vid.mp4"
FILENAME = './local_version/data/output/test_vid.avi'
CODEC = 'WMV1'
ASPECTPATH = "./local_version/data/input/aspect_test.mp4" #we can use that to show that the format thing works

 



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
        
        if isinstance(apply, nn.Module):
            img = video_preprocessing(img)
            apply(img)
            img = video_reprocessing(img)
        else:
            frame = apply(frame)

        #actual writing
        output.write(frame)

        cv.imshow('frame',frame)
        if cv.waitKey(1)== ord("d"):
            break
    source.release()
    output.release()
    cv.destroyAllWindows()