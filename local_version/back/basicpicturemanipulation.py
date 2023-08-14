#basic functions for the manipulation of pictures are done here

import cv2 as cv
 
def image_filter(path, apply, filename):

        #sometimes we encounter some reading issues while the image is not ready uploading, we don't want the programm to crash however. 
        try:
                img = cv.imread(path)
                img = apply(img)
                cv.imwrite(filename, img)
        except:
                print("Something went wrong appling the filter")



        
        

        
        


