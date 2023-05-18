import cv2 as cv
from filters import filter_gray

# loading and creating needed detectors and landmarks
harcascade = ("local_version/back/faceRec_files/haarcascade_frontalface_default.xml")
detector = cv.CascadeClassifier(harcascade)
LBFmodel = ("local_version/back/faceRec_files/lbfmodel.yaml")
landmark_detector = cv.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)

def get_coordinate (landmarks, face, mark):
    x = landmarks[face][0][mark][0]
    y = landmarks[face][0][mark][1]
    return (x,y)

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

def filter_clownNose(img):
    #read nose image and get ratio
    nose =  cv.imread("local_version/back/faceRec_files/filter_images/clown_nose.png")
    nose_height_ratio = nose.shape[0] / nose.shape[1]
    
    img_gray = filter_gray(img)
    faces = detector.detectMultiScale(img_gray)
    _,landmarks = landmark_detector.fit(img_gray, faces)

    # compute all necessary coordinates and values
    nose_middle = get_coordinate(landmarks, 0, 30)
    nose_right = get_coordinate(landmarks, 0, 35)
    nose_left = get_coordinate(landmarks, 0, 31)
    nose_width = int(nose_right[0] - nose_left[0])
    nose_height = int(nose_width * nose_height_ratio)
    new_nose = cv.resize(nose, dsize=(nose_width, nose_height), interpolation=cv.INTER_LINEAR)
    new_nose_topLeft = (int(nose_middle[0] - nose_width/2), int(nose_middle[1] - nose_height/2))
    new_nose_bottomRight = (int(nose_middle[0] + nose_width/2), int(nose_middle[1] + nose_height/2))

