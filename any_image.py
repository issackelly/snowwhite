#!/usr/bin/env python

#O Hai, it;s 8x8 lena

import opc, sys
from PIL import  Image

size = 16,16

im = Image.open(sys.argv[1])

## Layout.

## 1 [[0,0], [7,7]]    2 [[8,0][15, 7]]
## 3 [[8,0], [15,7]]   4 [[8,8][15, 15]]

sets = (
    ([0,0], [7,7]), # Top left
    [[8,0], [15,7]], # top right
    [[0,8], [7,15]], # bottom left
    [[8,8], [15,15]], # bottom right
)


client = opc.Client('localhost:7890')
black = [ (0,0,0) ] * size[0] * size[1]
client.put_pixels(black)


# crop to square
if im.size[0] > im.size[1]: # Landscape
    margin_left = int (( im.size[0] - im.size[1] ) / 2)
    im = im.crop((margin_left ,0, (margin_left + im.size[1] ),im.size[1]))
elif im.size[1] > im.size[0]:
    margin_top = int (( im.size[1] - im.size[0] ) / 2 )
    im = im.crop( (0, margin_top, im.size[0], (margin_top + im.size[0]) ) )

# resize
im.thumbnail(size, Image.NEAREST)
im.load()


lena = []

for start, end in sets:
    i = start[0]
    j = start[1]
    while j <= end[1]:
        while i <= end[0]:
            lena.append(im.getpixel((i,j)))
            i+=1
        j+=1
        i = start[0]

# Display the pixels
client.put_pixels(lena)
