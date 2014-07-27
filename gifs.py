from PIL import  Image
import sys
import opc, sys, time


from utils import size, layout, pil_resize_crop

from base import Pattern

MIN_SPEED = 0.15


class AnyGif(Pattern):

    def run(self, gif, **kwargs):

        black = [ (0,0,0) ] * size[0] * size[1]
        self.client.put_pixels(black)

        while self.redis_client.get('stop_pattern') == 'No':
            try:
                oim = Image.open(gif)
            except IOError:
                print "Cant load", gif
                break

            z = 0 # Frame
            speed = oim.info['duration'] / 1000


            if speed < MIN_SPEED:
                speed = MIN_SPEED
            mypalette = oim.getpalette()
            oim.putpalette(mypalette)
            try:
                while self.redis_client.get('stop_pattern') == 'No':
                    im = Image.new("RGBA", oim.size)
                    im.paste(oim)

                    im = pil_resize_crop(im, size)

                    pix = []

                    for start, end in layout:
                        i = start[0]
                        j = start[1]
                        while j <= end[1]:
                            while i <= end[0]:
                                pix.append(im.getpixel((i,j))[:3])
                                i+=1
                            j+=1
                            i = start[0]

                    # Display the pixels
                    self.client.put_pixels(pix)
                    time.sleep(speed)

                    z += 1
                    oim.seek(oim.tell() + 1)

            except EOFError:
                pass # end of sequence


if __name__ == '__main__':
    import opc, redis
    r = redis.Redis()

    client = opc.Client('localhost:7890')

    a = AnyGif(client, r)
    a.run(sys.argv[1])
