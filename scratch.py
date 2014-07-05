import opc, sys
from PIL import  Image
from utils import pil_resize_crop, layout, size

client = opc.Client('localhost:7890')
black = [ (0,0,0) ] * size[0] * size[1]

black[1] = (255, 255, 0)
black[512] = (255, 0, 0)
black[500] = (0,0,255)
client.put_pixels(black)

