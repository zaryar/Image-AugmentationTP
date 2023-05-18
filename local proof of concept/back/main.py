from filters import *
from videomanipulation import filter_video
from basicpicturemanipulation import image_filter
import time
import csv
import os


PATH = "./local proof of concept/front/public/images/input/"
FILENAME = './local proof of concept/front/public/images/output/'

IMAGE = "frame0.png"
VIDEO = "test_vid.mp4"


#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel }

def stream(PATH, filter,FILENAME):
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
                break


            
print(os.path.exists("./local proof of concept/front/public/config.csv"))

#READ CONFIG FILE
while True:
    file_exists = os.path.exists("./local proof of concept/front/public/config.csv")
    if file_exists:
        f = open("./local proof of concept/front/public/config.csv", newline='')
        #format = f.readline()
        format = "stream"
        filter = f.readline()
        print(format == "stream")
        print(type(format))
        os.remove("./local proof of concept/front/public/config.csv")
        if format == "stream":
            print(PATH, dict[filter] , FILENAME)
            stream(PATH, dict[filter], FILENAME)
        elif format == "video":
            
            filter_video(PATH + VIDEO, dict[filter], FILENAME + VIDEO)
        elif format == "picture":
            image_filter(PATH + IMAGE, dict[filter], FILENAME + IMAGE)

        print(dict[filter])
        

