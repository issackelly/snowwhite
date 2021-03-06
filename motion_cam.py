from SimpleCV import *
from PIL import  Image
import sys
import opc, sys, time
from SimpleCV.Features.HaarCascade import HaarCascade
from utils import simplecv_smart_crop


size = 32, 16
client = opc.Client('localhost:7890')


sets = (
    [[0,0], [7,7]],
    [[8,0], [15,7]],
    [[16,0],[23,7]],    #  0 1 2 3
    [[24,0],[31,7]],    #  4 5 6 7

    [[0,8], [7,15]],
    [[8,8], [15,15]],
    [[16,8],[23, 15]],
    [[24,8],[31,15]],
)

#cascade = HaarCascade("/home/issackelly/Projects/art/snowwhite/haarcascade_frontalface_default.xml")
#faces = im.findHaarFeatures(cascade)

# Initialize the camera
cam = Camera()
# Loop to continuously get images
last_im = cam.getImage()
while True:
    # Get Image from camera
    im = cam.getImage()
    nim = im - last_im
    last_im = im
    im = nim

    im = simplecv_smart_crop(im, size)

    # resize
    im = im.flipHorizontal()

    im = im.resize(*size)

    lena = []

    for start, end in sets:
        i = start[0]
        j = start[1]
        while j <= end[1]:
            while i <= end[0]:
                lena.append(im.getPixel(i,j))
                i+=1
            j+=1
            i = start[0]

    # Display the pixels
    client.put_pixels(lena)
    time.sleep(0.3)

