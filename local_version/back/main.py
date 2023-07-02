from filters import *
from faceRec_MP.mediapipeFilter import filter_clown, filter_dog, filter_video_clown, filter_video_dog, stream_face_recognition
from videomanipulation import filter_video, apply_faceRec_video
from basicpicturemanipulation import image_filter
import time
import csv
import os
import pandas as pd
import cv2
from fast_ns.experiments.filters_for_images import do_model, evaluate_img



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


#Types 
FACE_RECOGNITION = "FaceRecognition"
STYLE_TRANSFER = "StyleTransfer"
NORMAL_FILTER = "NormalFilter"

#Formats 
STREAM = "stream"
VID = "video"
IMG = "stream"

#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel,
        "filter4": filter_gray , "filter5" : filter_bw, "filter6" : filter_invert,
        "filter7": filter_sketch , "filter8" : filter_sepia, "filter9" : filter_sharp,
        "filter10": filter_edge , "filter11" : filter_border, "filter12" : filter_reflect,
        "filter13" : filter_wBorder,  
        "filter17" : filter_clown, "filter18": filter_dog, "filter19": filter_video_clown, "filter20": filter_video_dog}

def stream25(PATH, filter,FILENAME, model):
    stream_active = True
    while stream_active:
        path = PATH + FRAME
        if os.path.exists(LOCKIN): #is file ready?
            if not os.path.exists(LOCKOUT): #did we already display the last image?
                print(path, FILENAME, filter)         
                if model == NORMAL_FILTER:
                    image_filter(path, filter, FILENAME)
                else:
                    #stylize_image(path, filter, FILENAME, model)
                    return #@Valentin
                open(LOCKOUT, "x")
                file = FRAME
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
        time.sleep(0.04)


def read_config():
    config = pd.read_csv(CONFIG)
    config = config.to_string()
    
    counter = 0
    with open(CONFIG, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            if(counter == 0 ): #WARUM ?
                format = row[0]
                counter+=1
                continue
            if(counter == 1 ):
                filter = row[0]
                counter += 1
                continue
            type = row[0]
        print(type, filter, format)

    return format, type, filter

def translate_config(format, type, filter):
    if type == NORMAL_FILTER:
        if format == STREAM:
            stream25(PATH, dict[filter], FILENAME, NORMAL_FILTER)
        elif format == VID:
            filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)
        elif format == IMG:
            image_filter(PATH + IMAGE, dict[filter], OUTPUTPATH + IMAGE)

    elif type == FACE_RECOGNITION:
        if format == STREAM:
            stream_face_recognition(PATH, dict[filter], FILENAME)
        elif format == VID:
            filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)
        elif format == IMG:
            image_filter(PATH + IMAGE, dict[filter], OUTPUTPATH + IMAGE)

    elif type == STYLE_TRANSFER:

        models = do_model(filter) # Create models for StyleTransfer
        if format == STREAM:
            stream25(PATH, dict[filter], FILENAME, models)
        elif format == VID:
            filter_video(PATH + VIDEO, dict[filter], OUTPUTPATH + VIDEO)
        elif format == IMG:
            image_filter(PATH + IMAGE, dict[filter], OUTPUTPATH + IMAGE)



        



while True:
   
    time.sleep(1)
    print("Try to read: ", CONFIG)
    file_exists = os.path.exists(CONFIG)
    if file_exists:
        format, type, filter = read_config()

        if any(char.isdigit() for char in filter) and (STREAM in format or IMG in format or VID in format): 
            #print (dict[filter])
            #print(format)
            #print(type(format))
            translate_config(format, type, filter)


        else:
            print("wrong filter or format in config file!!")
            time.sleep(1)

        
        os.remove(CONFIG)
        time.sleep(0.1)
    else:
        print("no config file")
        time.sleep(0.1)

        
        