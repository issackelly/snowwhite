from PIL import  Image
import sys
import opc, sys, time
from utils import simplecv_smart_crop, layout, size

from base import Pattern

class Mirror(Pattern):

    def run(self, **kwargs):
        # Loop to continuously get images
        while self.redis_client.get('stop_pattern') == 'No':
            # Get Image from camera
            im = self.camera.getImage()

            im = simplecv_smart_crop(im, size)

            # resize
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
            self.client.put_pixels(frame)
            time.sleep(0.15) # 6.6 frames per second



if __name__ == '__main__':
    import opc, redis
    r = redis.Redis()
    client = opc.Client('localhost:7890')

    a = Mirror(client, r)
    a.run()
