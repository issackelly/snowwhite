from SimpleCV import Camera
from PIL import  Image
import sys
import opc, sys, time
from utils import simplecv_smart_crop, layout, size

client = opc.Client('localhost:7890')


# Initialize the camera
cam = Camera()
# Loop to continuously get images

opening_im = simplecv_smart_crop(cam.getImage(), size)
while True:
    # Get Image from camera
    im = cam.getImage()

    im = simplecv_smart_crop(im, size)

    # resize
    im = (opening_im - im).grayscale()

    im = im.flipHorizontal()
    im = im.resize(*size)

    frame = []

    for start, end in layout:
        i = start[0]
        j = start[1]
        while j <= end[1]:
            while i <= end[0]:
                frame.append(im.getPixel(i,j))
                i+=1
            j+=1
            i = start[0]

    # Display the pixels
    client.put_pixels(frame)
    time.sleep(0.15)
