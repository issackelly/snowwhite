#!/usr/bin/env python
import opc, sys
from PIL import  Image
from utils import pil_resize_crop, layout, size
from base import Pattern

class AnyImage(Pattern):

    def run(self, image, **kwargs):
        im = Image.open(image)
        black = [ (0,0,0) ] * size[0] * size[1]
        self.client.put_pixels(black)

        im = pil_resize_crop(im, size)

        pix = []

        for start, end in layout:
            i = start[0]
            j = start[1]
            while j <= end[1]:
                while i <= end[0]:
                    pix.append(im.getpixel((i,j))[:3]) # Only want RGB, not RGBA
                    i+=1
                j+=1
                i = start[0]

        # Display the pixels
        self.client.put_pixels(pix)

if __name__ == '__main__':
    import opc

    client = opc.Client('localhost:7890')

    a = AnyImage(client)
    a.run(sys.argv[1])
