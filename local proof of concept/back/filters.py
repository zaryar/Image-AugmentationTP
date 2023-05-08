import cv2 as cv
import numpy as np

# given img becomes Grayscale
def filter_gray(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return gray

# given img becomes black and white
def filter_bw(img):
    gray = filter_gray(img)
    _, bw = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
    return bw

# given img becomes invertet
def filter_invert(img):
    invert = cv.bitwise_not(img)
    return invert

# given img becomes sketched
def filter_sketch(img):
    _, sketch = cv.pencilSketch(img, sigma_s=7, sigma_r=0.8, shade_factor=0.03)
    return sketch

# given img gets different colored overlay
# blue, green, red decide the overlays color
# intensity decides intensity of the overlay
def filter_color_overlay(img, blue, green, red, intensity):
    image = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    width, height, channels = image.shape
    newBGRA = (blue, green, red, 1)
    overlay = np.full((width, height, channels), newBGRA, dtype='uint8')
    cv.addWeighted(overlay, intensity, image, 1.0, 0, image)
    image = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    return image

# given img becomes pixelated
# pixels are pixelsize x pixelsize large
def filter_pixel(img):
    gray = filter_gray(img)
    height, width = gray.shape
    pixelSize = 10
    newWidth = width // pixelSize
    newHeight = height // pixelSize
    pixel = cv.resize(img, dsize=(newWidth, newHeight), interpolation=cv.INTER_LINEAR)
    pixel = cv.resize(pixel, dsize=(width, height), interpolation=cv.INTER_NEAREST)
    return pixel

# given img becomes blurry
# ksize=(x,y) decides how many surrounding pixels get effected on x and y axis (bigger number more blurred)
def filter_blurred(img):
    gray = filter_gray(img)
    height, width = gray.shape
    effect = int((height+width) / 100)
    blurred = cv.blur(img, ksize=(effect,effect))
    return blurred

# given img becomes blurry
# array decides how neighbour pixels get effected (middle pixel needs to be bigger value than surrounding pixels combined)
# left, right, top, bottom pixels need to be negative, middle positive
def filter_sharp(img):
    neighbor = -1
    middle = neighbor * -4 + 1
    sharpen = np.array([
        [0,neighbor,0],
        [neighbor,middle,neighbor],
        [0,neighbor,0]
    ])
    sharp = cv.filter2D(img, ddepth = -1, kernel = sharpen)
    return sharp

# detects edges from given Image
# array decides how neighbour pixels get effected (middle pixel needs to be smaller value than surrounding pixels combined)
# surrounding pixels need to be negative, middle positive
def filter_edge(img):
    gray = filter_gray(cv.GaussianBlur(img, ksize=(3,3), sigmaX=2, sigmaY=2)) # for white edges 
    neighbor = -4
    middle = neighbor * -8 -0.1
    edges = np.array([
        [neighbor,neighbor,neighbor],
        [neighbor,middle,neighbor],
        [neighbor,neighbor,neighbor]
    ])
    edge = cv.filter2D(gray, ddepth = -1, kernel = edges)
    #edge = cv.Laplacian(gray, ddepth=-1)  #other way for edges not using filter2D but not as visible
    return edge

# rotates image 90 degrees clockwise 
def filter_rotate(img):
    rotate = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    return rotate

# adds a border in dark purple
def filter_border(img, blue, green, red):
    borderWidth = 50
    border = cv.copyMakeBorder(img, borderWidth, borderWidth, borderWidth, borderWidth, borderType=cv.BORDER_CONSTANT, value=(blue, green, red))
    return border

# adds a reflection top, left
def filter_reflect(img):
    gray = filter_gray(img)
    height, width = gray.shape
    reflect = cv.copyMakeBorder(img, 0, height, width, 0, borderType=cv.BORDER_REFLECT)
    return reflect

# repeats image top left
def filter_wBorder(img):
    gray = filter_gray(img)
    height, width = gray.shape
    wBorder = cv.copyMakeBorder(img, 0, height, width, 0, borderType=cv.BORDER_WRAP)
    return wBorder

# flips the image
# flip value 0 = xaxis, 1 = yaxis, -1 = both
def filter_flip(img):
    flip = cv.flip(img, -1)
    return flip