from SimpleCV import *
from PIL import  Image as PImage
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

cascade = HaarCascade("/home/issackelly/Projects/art/snowwhite/haarcascade_frontalface_default.xml")

# Initialize the camera
cam = Camera()
# Loop to continuously get images
while True:
    # Get Image from camera
    im = cam.getImage()


    # crop to square
    im = simplecv_smart_crop(im, size)
    im = im.flipHorizontal()

    nim = im - im
    nim = nim.getPIL()
    nim.thumbnail(size, PImage.NEAREST)

    nim = nim.load()

    faces = im.findHaarFeatures(cascade)
    for f in faces:
        i = int(f.x * (size[0] / im.width))
        j = int(f.y * (size[1] / im.height))
        while j < int(f.height() * (size[1] / im.height)):
            while i < int(f.width() * (size[0] / im.width)):
                print i, j
                nim[i,j] = (255, 255, 255)
                i+=1
            i = f.x
            j+=1


    lena = []

    for start, end in sets:
        i = start[0]
        j = start[1]
        while j <= end[1]:
            while i <= end[0]:
                try:
                    lena.append(nim[i,j])
                except:
                    lena.append((0,0,0))
                    #print '***'
                    pass
                #print i,j
                i+=1
            j+=1
            i = start[0]

    # Display the pixels
    client.put_pixels(lena)
    time.sleep(0.001)

