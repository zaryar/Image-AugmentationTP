import cv2 as cv
from filters import filter_gray

# loading and creating needed detectors and landmarks
harcascade = ("local_version/back/faceRec_files/haarcascade_frontalface_default.xml")
detector = cv.CascadeClassifier(harcascade)
LBFmodel = ("local_version/back/faceRec_files/lbfmodel.yaml")
landmark_detector = cv.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)

# creates landmarks and shows as green dots
def filter_landmarks(img):
    img_gray = filter_gray(img)
    faces = detector.detectMultiScale(img_gray)
    _,landmarks = landmark_detector.fit(img_gray, faces)
    for landmark in landmarks:
        for x,y in landmark[0]:
            cv.circle(img, (int(x),int(y)), 1, (0, 255, 0), 2)
    return img

# creates landmarks and shows as green numbers
# to see which landmarks are where
def filter_numbers(img):
    img_gray = filter_gray(img)
    faces = detector.detectMultiScale(img_gray)
    _,landmarks = landmark_detector.fit(img_gray, faces)
    counter = 0
    for landmark in landmarks:
        for x,y in landmark[0]:
            cv.putText(img, str(counter), (int(x),int(y)), cv.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1, cv.LINE_AA)
            counter = counter + 1
    return img
