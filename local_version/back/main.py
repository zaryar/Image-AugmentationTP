from filters import *
from videomanipulation import filter_video
from basicpicturemanipulation import image_filter
import time
import csv
import os
import pandas as pd


PATH = "./local_version/front/public/images/input/"
FILENAME = './local_version/front/public/images/output/'
CONFIG = "./local_version/front/public/config.csv"

IMAGE = "frame.png"
VIDEO = "test_vid.mp4"


#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel }

def stream25(PATH, filter,FILENAME):
    frame_available = True
    while frame_available:
        for frame in range(25):
            path = PATH + "frame" + str(frame) + ".png"
            print(PATH)
            filename = FILENAME + "frame" + str(frame) + ".png"
            if os.path.exists(path):            
                image_filter(path, filter, filename)
                os.remove(path)
            else: 
                time.sleep(0.05)
                if False == os.path.exists(PATH):
                    frame_available = False
                    break

def stream(PATH, filter, FILENAME):
    frame_available = True
    while frame_available:
        path = PATH + IMAGE
        filename = FILENAME + IMAGE
        print(path, filename)
        if os.path.exists(path):            
                image_filter(path, filter, filename)
                #os.remove(path)
        else: 
            time.sleep(0.05)
            if os.path.exists(path):            
                image_filter(path, filter, filename)
                #os.remove(path)
            else:
                frame_available = False

            

print(os.path.exists(CONFIG))

#READ CONFIG FILE
while True:
    file_exists = os.path.exists(CONFIG)
    if file_exists:
        config = pd.read_csv(CONFIG)

        print(config)
        format = "stream"
        filter = "filter2"
        print (dict[filter])
        print(format == "stream")
        print(type(format))

        os.remove(CONFIG)
        if format == "stream":
            print(PATH, dict[filter] , FILENAME)
            stream(PATH, dict[filter], FILENAME)
        elif format == "video":
            
            filter_video(PATH + VIDEO, dict[filter], FILENAME + VIDEO)
        elif format == "picture":
            image_filter(PATH + IMAGE, dict[filter], FILENAME + IMAGE)

        print(dict[filter])
        

