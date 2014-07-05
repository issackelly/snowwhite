from PIL import  Image
import sys
import opc, sys, time


from utils import size, layout, pil_resize_crop

client = opc.Client('localhost:7890')
black = [ (0,0,0) ] * size[0] * size[1]
client.put_pixels(black)

MIN_SPEED = 0.15


while True:
    try:
        oim = Image.open(sys.argv[1])
    except IOError:
        print "Cant load", infile
        sys.exit(1)
    z = 0 # Frame
    speed = oim.info['duration'] / 1000


    if speed < MIN_SPEED:
        speed = MIN_SPEED
    mypalette = oim.getpalette()
    oim.putpalette(mypalette)
    try:
        while True:
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
            client.put_pixels(pix)
            time.sleep(speed)

            z += 1
            oim.seek(oim.tell() + 1)

    except EOFError:
        pass # end of sequence
