#!/usr/bin/env python

import opc, sys
from PIL import  Image
from utils import pil_resize_crop, layout, size

def blank():
    client = opc.Client('localhost:7890')
    black = [ (0,0,0) ] * size[0] * size[1]
    client.put_pixels(black)


if __name__ == '__main__':
    blank()
