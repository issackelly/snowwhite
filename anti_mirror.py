from SimpleCV import Camera
from PIL import  Image
import sys
import opc, sys, time
from utils import simplecv_smart_crop, layout, size

from blank import Blank
from base import Pattern

import datetime

class AntiMirror(Pattern):

    def run(self, **kwargs):
        last_orig = datetime.datetime.now()
        orig_timeout = datetime.timedelta(seconds=10)

        blank = Blank(self.client)

        # Loop to continuously get images
        opening_im = simplecv_smart_crop(self.camera.getImage(), size)
        threshold = 9.0 # if mean exceeds this amount do something

        while self.redis_client.get('stop_pattern') == 'No':
            # Get Image from camera
            im = self.camera.getImage()

            im = simplecv_smart_crop(im, size)

            # resize
            im = im.flipHorizontal()

            diff = im - opening_im
            matrix = diff.getNumpy()
            mean = matrix.mean()


            if mean >= threshold:
                im = im.resize(*size)
                diff = im.resize(*size)
                frame = []

                for start, end in layout:
                    i = start[0]
                    j = start[1]
                    while j <= end[1]:
                        while i <= end[0]:
                            frame.append(diff.getPixel(i,j))
                            i+=1
                        j+=1
                        i = start[0]
                # Display the pixels
                self.client.put_pixels(frame)
            else:
                print mean
                blank.run()

            if (last_orig + orig_timeout) < datetime.datetime.now():
                print "updating image"
                last_orig = datetime.datetime.now()
                opening_im = simplecv_smart_crop(self.camera.getImage(), size)


            time.sleep(0.15)



if __name__ == '__main__':
    import opc, redis
    r = redis.Redis()
    client = opc.Client('localhost:7890')

    a = AntiMirror(client, r)
    a.run()
