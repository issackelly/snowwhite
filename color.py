#!/usr/bin/env python

import opc, sys
from PIL import  Image
from utils import pil_resize_crop, layout, size

from base import Pattern

class Color(Pattern):
    def run(self, color, **kwargs):

        if isinstance(color, basestring):
            color = [int(i) for i in color.split(", ")]

        pattern = [ color ] * size[0] * size[1]
        self.client.put_pixels(pattern)
        self.client.put_pixels(pattern) # Not sure why I have to run this twice.


if __name__ == '__main__':
    import opc
    client = opc.Client('localhost:7890')

    a = Color(client)
    a.run(sys.argv[1])
