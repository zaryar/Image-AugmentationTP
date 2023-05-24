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

def paste_image (top, bottom, left, right, img, front):
    front_gray = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
    _, mask= cv.threshold(front_gray, 200, 255, cv.THRESH_BINARY)
    roi = img[top:bottom, left:right]
    inverseMask = cv.bitwise_not(mask)
    background = cv.bitwise_and(roi, roi, mask = mask)
    frontImage = cv.bitwise_and(front, front, mask = inverseMask)
    dst = cv.add(background, frontImage)
    img[top:bottom, left:right] = dst
    
    return img

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
    nose =  cv.imread("local_version/back/faceRec_files/filter_images/clownNose.png")
    nose_height_ratio = nose.shape[0] / nose.shape[1]
    
    img_gray = filter_gray(img)
    faces = detector.detectMultiScale(img_gray)
    _,landmarks = landmark_detector.fit(img_gray, faces)

    # compute all necessary coordinates and values
    nose_middle = get_coordinate(landmarks, 0, 30)
    nose_right = get_coordinate(landmarks, 0, 35)
    nose_left = get_coordinate(landmarks, 0, 31)
    nose_width = int((nose_right[0] - nose_left[0])*1.2)
    nose_height = int(nose_width * nose_height_ratio)
    new_nose = cv.resize(nose, dsize=(nose_width, nose_height), interpolation=cv.INTER_LINEAR)

    # get the necessary filter coordinates
    new_nose_left = int(nose_middle[0] - nose_width/2)
    new_nose_right = int(new_nose_left + nose_width)
    new_nose_top = int(nose_middle[1] - nose_height/2)
    new_nose_bottom = int(new_nose_top + nose_height)

    # paste filter into image
    img = paste_image(new_nose_top, new_nose_bottom, new_nose_left, new_nose_right, img, new_nose)

    return img

def filter_mustache(img):
    #read mustache image and get ratio
    mustache =  cv.imread("local_version/back/faceRec_files/filter_images/mustach.png")
    mustache_height_ratio = mustache.shape[0] / mustache.shape[1]
    
    img_gray = filter_gray(img)
    faces = detector.detectMultiScale(img_gray)
    _,landmarks = landmark_detector.fit(img_gray, faces)

    # compute all necessary coordinates and values
    lip_top = get_coordinate(landmarks, 0, 51)
    nose_bottom = get_coordinate(landmarks, 0, 33)
    middle_lip_nose = (lip_top[1] - int((lip_top[1] - nose_bottom[1])/4))
    mustache_middle = [lip_top[0], middle_lip_nose]
    mustache_right = get_coordinate(landmarks, 0, 54)
    mustache_left = get_coordinate(landmarks, 0, 48)
    mustache_width = int((mustache_right[0] - mustache_left[0])*1.2)
    mustache_height = int(mustache_width * mustache_height_ratio)
    new_mustache = cv.resize(mustache, dsize=(mustache_width, mustache_height), interpolation=cv.INTER_LINEAR)

    # get the necessary filter coordinates
    new_mustache_left = int(mustache_middle[0] - mustache_width/2)
    new_mustache_right = int(new_mustache_left + mustache_width)
    new_mustache_top = int(mustache_middle[1] - mustache_height/2)
    new_mustache_bottom = int(new_mustache_top + mustache_height)

    # paste filter into image
    img = paste_image(new_mustache_top, new_mustache_bottom, new_mustache_left, new_mustache_right, img, new_mustache)

    return img