from filters import *
from videomanipulation import filter_video
import os


PATH = "./local_proof_of_concept/front/public/images/input/test_vid.mp4"
FILENAME = './local_proof_of_concept/front/public/images/output/test_vid.mp4'

#Translation Test Dictionary

dict = {"filter1": filter_blurred , "filter2" : filter_flip, "filter3" : filter_pixel }

#READ CONFIG FILE
while True:
    file_exists = os.path.exists("./local_proof_of_concept/front/public/configData.txt")
    if file_exists:
        f = open("./local_proof_of_concept/front/public/configData.txt","r")
        format = f.readline()
        filter = f.readline()
        os.remove("./local_proof_of_concept/front/public/configData.txt")
        print(dict[filter])
        filter_video(PATH, dict[filter], FILENAME)

