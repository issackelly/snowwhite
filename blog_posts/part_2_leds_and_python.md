#Snow White Part 2: Driving LEDs with Python

The state of python on embedded systems isn't great. That's not bad news though!
Raspberry Pis are cheap and run python pretty darn well.

If you want to drive a single LED on a Rasperry Pi with python, I'm not going to cover that here.
I'm going to talk about running a few thousand LEDs, but let's start with some basics.

I like[1] the World Semi set of LEDs called the WS281X series, there are several variations, and working
with them with an arduino is REALLY straight forward. Adafruit sells several variations of these under the "NeoPixel" brand name. Sparkfun sells them too. You can get them from way cheaper from vendors in China off of AliExpress if you are patient and trusting.

If you want to code these in python, there is a special brand of microcontroller which makes it really easy.
Micah Scott created a project called (FadeCandy)[https://github.com/scanlime/fadecandy/] based on a Teensy Microcontroller (Arduino Compatible, Open Source, ARM chipset).

Fadecandy, combined with (Open Pixel Control)[http://openpixelcontrol.org/] make it very simple to control a string of serial LEDs from many languages, python included.

Fadecandy costs about $24 from Adafruit or Sparkfun and can drive 512 of these serial LEDs on 8 different channels (64 in series per channel, though that's abstracted from you). It's as easy as building a python list of LEDs and their associated RGB value, and feeding that to a python client which is as simple as requests.

FadeCandy boards plug into USB, and you can run tons of them off of the same computer. A simple config file manages the locations of the channels. A single process runs an OPC server and spits all the right values to the right channels to color your display, whatever the configuration.

Open Pixel Control also includes an OpenGL sample server. You can view a simple representation of your LED display and test it and write code for it while you're on vacation, and when you get back to your device several weeks later, you won't be surprised at how it looks.

What I mean to say is, You get to stand on the shoulders of giants if you are trying to write python (or many other languages) to interface with LEDs in any configuration you can imagine. If you can imagine and wire your LEDs in a single line, Linux, OpenPixel, FadeCandy, and WS281(1|2)[ab]{0,1} LEDs can make this a reality.

I built a python script for turning the adafruit grids of LEDs into an OpenPixel layout for the OpenGl server. That is on (this file)[https://github.com/issackelly/snowwhite/blob/master/opc/opc_layout.py].

Now that we're this far, what I'm saying, is buy a fadecandy board, and run a fadecandy server and all of this gets super easy. A fadecandy board and some LEDs will cost you anywhere from $40 to $200.

The LEDs that I used were arranged in an array, but as far as the LEDs are concerned, and how they pass data, they're arranged in a line.

The Adafruit NeoPixel 8x8 Matrix looks like this

    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o
    o    o    o    o    o    o    o    o

But it's arranged like this


    0    1    2    3    4    5    6    7
    8    9   10   11   12   13   14   15
    16  17   18   19   20   21   22   23
    24  25   26   27   28   29   30   31
    32  33   34   35   36   37   38   39
    40  41   42   43   44   45   46   47
    48  49   50   51   52   53   54   55
    56  57   58   59   60   61   62   63

The LEDs think they're in a line.

You need to compensate for this if you want to make 2D art. Not all display matrices are set up like this, but these are.


Let's make the canvas of a single array blue. First, run a fadecandy server (read her readme for this).

Next, copy the OPC.py from her examples folder or my code into your project.

Now we'll write the following in a python shell

    import opc
    pattern = [ 0, 0, 255 ] * 8 * 8
    client = opc.Client('localhost:7890')
    client.put_pixels(pattern)

If everything is hooked up correctly, your display will be blue.

You might recognize the 3-tuple from line 2 as an RGB value. An RGB value is a set of three numbers, typically from 0-255 for mathetical reasons regarding powers of 2. This one says "this color is 0% red, 0% green, and 100% blue". Colors from a display are a mixture of red green and blue, and from these three your eye understands a variety of colors. If you're interested in this concept you should explore pointalism, modern dispalys work in the same way.

Let's make something slightly more recognizable. Or less. I made a silly image of pink and green and white.

You don't get much resolution at 8 by 8.

If you start with an image of 8 by 8 you can just open it up with PIL and read every RGB value and put that back to the client.

    import opc
    client = opc.Client('localhost:7890')

    im = Image.open('~/path/to/image.png')

    i = 0
    j = 0
    pix = []
    while j <= 7:
        while i <= 7:
            pix.append(im.getpixel((i,j))[:3]) # Only want RGB, not RGBA
            i+=1
        j+=1
        i = 0
    client.put_pixels(pix)

I'm going to skip over the pil stuff, that's in the next post.

This is a pretty naiive algorithm which iterates over the top left of an image which is greater or equal to 8x8px. This reads the first 64 pixels, in the same pattern as our led array. It makes a single list, which it sends to the OPC server.

This is roughly all you need to start Writing to LEDs with python, NeoPixels and Fadecandy.


Next up: Image Manipulation.


My code is ugly! My writing is bad! As always, email me your feedback! I love to hear from people who read my posts, and I'd like to edit things that are wrong or unclear.


[1] Mostly, There are caveats to using these at scale, full-time, but they're beyond
the scope of these posts. If you're super intereseted in using these for an installation,
let me know and we can discuss the positives and negatives, maybe it will be a future post.
