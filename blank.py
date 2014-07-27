#!/usr/bin/env python

import opc, sys
from PIL import  Image
from utils import pil_resize_crop, layout, size

from base import Pattern

class Blank(Pattern):
    def run(self, **kwargs):
        black = [ (0,0,0) ] * size[0] * size[1]
        self.client.put_pixels(black)
        self.client.put_pixels(black) # Not sure why I have to run this twice.


if __name__ == '__main__':
    import opc
    client = opc.Client('localhost:7890')

    a = Blank(client)
    a.run()
