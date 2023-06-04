from filters import *
from videomanipulation import filter_video
from basicpicturemanipulation import image_filter
import time
import csv
import os
import pandas as pd


PATH = "./local_version/front/public/images/input/"
FILENAME = './local_version/front/public/images/output/frame.png'
CONFIG = "./local_version/front/public/config.csv"
STOPP = "./local_version/front/public/stop.txt"

FRAME = "frame.png"
IMAGE = "image.png"
VIDEO = "test_vid.mp4"


#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel }

def stream25(PATH, filter,FILENAME):
    stream_active = True
    while stream_active:
        path = PATH + "frame.png"
        if os.path.exists(path):
            print(path, FILENAME, filter)
            image_filter(path, filter, FILENAME)
            file = 'frame.png'
            os.remove(os.path.join(PATH, file))      
        stream_active = os.path.exists(STOPP) == False
        time.sleep(0.04)
             


def stream(PATH, filter, FILENAME):
    frame_available = True
    while frame_available:
        path = PATH + FRAME
        filename = FILENAME + IMAGE
        print(path, filename)
        if os.path.exists(path):            
                image_filter(path, filter, filename)
                time.sleep(1)
                # os.remove(path)
        else: 
            time.sleep(4)
            if os.path.exists(path):            
                image_filter(path, filter, filename)
                #os.remove(path)
            else:
                frame_available = False

            

print(os.path.exists(CONFIG))
print(os.path.exists('./front/public/config.csv'))

#READ CONFIG FILE
while True:
    file_exists = os.path.exists(CONFIG)
    if file_exists:
        config = pd.read_csv(CONFIG)
        config = config.to_string()
        
        format = "stream"
        filter = "filter3"
        print (dict[filter])
        print(format == "stream")
        print(type(format))

        os.remove(CONFIG)
        if format == "stream":
            print(PATH, dict[filter], FILENAME)
            stream25(PATH, dict[filter], FILENAME)
        elif format == "video":
            
            filter_video(PATH + VIDEO, dict[filter], FILENAME + VIDEO)
        elif format == "picture":
            image_filter(PATH + IMAGE, dict[filter], FILENAME + IMAGE)

        print(dict[filter])
        