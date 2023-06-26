from filters import *
from fast_neural_style.neural_style.neural_style import filter_candy, filter_monet, filter_starry_night
from faceRec_MP.mediapipeFilter import filter_clown, filter_dog, filter_video_clown, filter_video_dog
from videomanipulation import filter_video, apply_faceRec_video
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
LOCKOUT = './local_version/front/public/images/output/lockOut'
LOCKIN = './local_version/front/public/images/input/lockIn'


FRAME = "frame.png"
IMAGE = "image.png"
VIDEO = "test_vid.mp4"


#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel,
        "filter4": filter_gray , "filter5" : filter_bw, "filter6" : filter_invert,
        "filter7": filter_sketch , "filter8" : filter_sepia, "filter9" : filter_sharp,
        "filter10": filter_edge , "filter11" : filter_border, "filter12" : filter_reflect,
        "filter13" : filter_wBorder, "filter14": filter_candy, "filter15": filter_starry_night, "filter16": filter_monet,
        "filter17" : filter_clown, "filter18": filter_dog, "filter19": filter_video_clown, "filter20": filter_video_dog}

def stream25(PATH, filter,FILENAME):
    stream_active = True
    while stream_active:
        path = PATH + "frame.png"
        if os.path.exists(LOCKIN): #is file ready?
            if not os.path.exists(LOCKOUT): #did we already display the last image?
                print(path, FILENAME, filter)         


                image_filter(path, filter, FILENAME)
                open(LOCKOUT, "x")
                file = 'frame.png'
                os.remove(os.path.join(PATH, file))
                os.remove(LOCKIN) #remove the ability to work with file
            else:
                print("lockOut already there | not worked with on canvis")
        else:
            print("input file cant be found")
        stream_active = os.path.exists(STOPP) == False
        if os.path.exists(STOPP):
            #os.remove(CONFIG)
            os.remove(STOPP)
            return
        time.sleep(0.3)
             

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
    time.sleep(1)
    print("Try to read: ", CONFIG)
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
                if(counter == 1):
                    filter = row[0]  
                    counter+=1
                    continue
                if(counter == 2):
                    typ = row[0]  
                    counter+=1
                    continue

        if any(char.isdigit() for char in filter) and ("stream" in format or "image" in format or "video" in format): 
            print (dict[filter])
            print(format)
            #print(type(format))

            #os.remove(CONFIG)
            if format == "stream":
                #print(PATH, dict[filter], FILENAME)
                stream25(PATH, dict[filter], FILENAME)

            elif format == "video":
                if typ == "NormalFilter":
                    filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)
                elif typ == "StyleTransfer":
                    filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)
                else:
                    apply_faceRec_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)

            elif format == "image":
                image_filter(PATH + IMAGE, dict[filter], OUTPUTPATH + IMAGE)

        else:
            print("wrong filter or format in config file!!")
            time.sleep(1)
        
        
        os.remove(CONFIG)
        time.sleep(1)
    else:
        print("no config file")
        time.sleep(1)

        
        