#!/usr/bin/env python

import redis
import opc

#Shared camrea
from SimpleCV import Camera
camera = Camera()

client = opc.Client('localhost:7890')
r = redis.Redis()


from gifs import AnyGif
from any_image import AnyImage
from anti_mirror import AntiMirror
from camera import Mirror
from blank import Blank
from tetris import Tetris
from color import Color

patterns = {
    "gif": AnyGif(client, r),
    "image": AnyImage(client),
    "mirror": Mirror(client, r, camera),
    "antimirror": AntiMirror(client, r, camera),
    "blank": Blank(client),
    "color": Color(client),
    "tetris": Tetris(client, r),
}

def run():
    global r

    last_pattern = None

    while True:
        pattern = patterns.get(r.get('pattern'), None) or None
        if (pattern != last_pattern) or (r.get('stop_pattern') == 'Yes'):
            r.set('stop_pattern', 'No')
            args = r.hgetall('patternargs')
            last_pattern = pattern
            pattern.run(**args)


if __name__ == '__main__':
    while True:
        try:
            run()
        except:
            pass
