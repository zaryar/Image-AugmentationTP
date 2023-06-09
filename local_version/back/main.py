from filters import *
from videomanipulation import filter_video
from basicpicturemanipulation import image_filter
import time
import csv
import os
import pandas as pd

import cv2



PATH = "./local_version/front/public/images/input/"
OUTPUTPATH = "./local_version/front/public/images/output/"
FILENAME = './local_version/front/public/images/output/frame.png'
CONFIG = "./local_version/front/public/config.csv"
STOPP = "./local_version/front/public/stopStream.txt"


FRAME = "frame.png"
IMAGE = "image.png"
VIDEO = "test_vid.mp4"


#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel,
        "filter4": filter_gray , "filter5" : filter_bw, "filter6" : filter_invert,
        "filter7": filter_sketch , "filter8" : filter_sepia, "filter9" : filter_sharp,
        "filter10": filter_edge , "filter11" : filter_border, "filter12" : filter_reflect,
        "filter13" : filter_wBorder}

def stream25(PATH, filter,FILENAME):
    stream_active = True
    while stream_active:
        path = PATH + "frame.png"
        if os.path.exists(path) and not os.path.exists(FILENAME):
            print(path, FILENAME, filter)
            
 
            try:
                img = cv2.imread("./local_version/front/public/images/input/frame.png", cv2.IMREAD_UNCHANGED)
                print('Original Dimensions : ',img.shape)
                scale_percent = 5 # percent of original size
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv.imwrite("./local_version/front/public/images/input/frame.png", img)
            except:
                print("did not resize")
            

            image_filter(path, filter, FILENAME)
            file = 'frame.png'
            os.remove(os.path.join(PATH, file))
        stream_active = os.path.exists(STOPP) == False
        if os.path.exists(STOPP):
            #os.remove(CONFIG)
            os.remove(STOPP)
            return
             

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

            

#print(os.path.exists(CONFIG))
#print(os.path.exists('./front/public/config.csv'))

#READ CONFIG FILE
while True:
    file_exists = os.path.exists(CONFIG)
    if file_exists:
        config = pd.read_csv(CONFIG)
        config = config.to_string()
        
        counter = 0
        with open(CONFIG, "r") as csvFile:
            csvReader = csv.reader(csvFile)
            for row in csvReader:
                if(counter == 0 ):
                    format = row[0]
                    counter+=1
                    continue
                filter = row[0]        

        if "filter" in filter and ("stream" in format or "image" in format or "video" in format): 
            print (dict[filter])
            print(format)
            #print(type(format))

            #os.remove(CONFIG)
            if format == "stream":
                #print(PATH, dict[filter], FILENAME)
                stream25(PATH, dict[filter], FILENAME)

            elif format == "video":
                filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)

            elif format == "image":
                image_filter(PATH + IMAGE, dict[filter], OUTPUTPATH + IMAGE)

        else:
            print("wrong filter or format in config file!!")
            time.sleep(1)
        
        
        os.remove(CONFIG)
        time.sleep(0.4)
    else:
        print("no config file")
        time.sleep(1)

        
        