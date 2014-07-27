Concept:

I wanted to share what it's like building art and electronics projects with python.

Most of my work is for a very private social organization, It's difficult to discuss.

So I made something up for you. It's sort of intentionally devoid of artistic vision.
If I were applying for a grant, I'd spend another several hundred words about how
meaningful that was.

You can make it whatever you want, it's more of a canvas for building your own piece.

So far I've made several pieces with it, ranging from the utterly silly to some
which are personally a little more....reflective.

Anyway, without further adieu, here's snow white.

------

(unveil....ooohhh...ahhh from computer audio)

------

I call it an autoreflector. Cute right? At least when I'm looking, and at least while it's off.

Anyway, Let's turn it on.

(full white)

As you can maybe tell now, this is what is moronically called two-way glass. Glass by nature is two-way.
This is more like "conditionally one-way glass". The condition is that it's dark on one side. That side
can see out, but the light side can't see in. If you've seen a cop drama, you probably get the idea.

This one isn't even glass, it's acrylic. It travels better and is less likely to cut me open.

I got this cut to fit the thrift-shop frame from my local plastics store.

Let's get the practical considerations of the medium out of the way before we dig into the software.

We have some two way glass, and an array of LEDs. That's about it for this piece.
Affixed to one side of the glass is some vellum paper.
This diffuses the light from the other side so you don't see pixels.
This is so we get more of an impression than an array.

-------

So, you've got this crazy idea for a piece of hardware, or some interactive art,
and so One might think think to Oneself:

    ooh, simple, it's just some two way glass, and some LEDs. Probably like, a weekend's
    worth of work.

Then the reality sets in.

You still have to:

Pick the format () {} [] [  ] o
Pick the leds ---- [ ] ...
Adjust the format
Pick the Power Supply
Pick the driver(s)
Estimate the cost.
Panic. Adjust. Unpanic.
Pick the logic controller (hardware and software)
Prototype the hardware
    * Design custom breakouts
    * Order a few from a fab ( 2 weeks )
    * Test Those
    * Order a few dozen from a fab ( 2 weeks )
Prototype the software
Build the mounting brackets
Assemble the pieces
Build the wiring harnesses
Finish the software
Ship it to Ohio
...
Present the Project
Come to grips with the budget

What I'm here to tell you is that knowing how to program, and specifically knowing Python
makes this part, and all the little unknowns WAY more manageable.

I used python for:
* Designing/Cutting the Mounting Bracket
* Prototyping visual manipulation
* Computer Vision
* Super Silly Gif Playing
* Super Sillier Tetris Game
* Super Silliest Multi-player Tetris Server
* Building the layout for the open pixel control demo server

So, for a little more deconstruction:
    The mounting boards are laser cut from 1/8" clear acrylic. Hindsight says
    I should have used opaque acrylic instead of clear. It's a little more expensive,
    but it will block out the light better.

    The acrylic is all cut to fit around the edge of the mirror, and for the arrays
    to be within 1mm of each other, and to all have their screw holes available for mounting

    There are 20 Adafruit NeoPixel Arrays.
        Each array has 64 pixels, connected together in a line, Its embedded software thinks
        in 1 dimension, but it's arranged in two dimensions. This provides some interesting
        mental gymnastics to display two-d images. (visual)

    NeoPixels are Adafruit's brand name for their WS2812 line of RGB LEDs with an integrated circuit
    inside.

    The Adafruit NeoPixel arrays get headers soldered to the DIN side.

    Each array gets one pin on a FadeCandy board.
        FadeCandy is a project by Micah Scott. It's a USB connected board that will drive up to 512 of
        LEDS through 8 channels.
        FadeCandy also has an Open Pixel server which runs on the computer, and tons of python (and go, and c and processing) example code.
        Open Pixel Control is a protocol, server, and mock library for working with these types of systems.

    Nylon M3 screws and nuts are used to attach each array to the mounting board.

    Each board got a breakout.
    Each breakout got a 3 position screw terminal and some solder.

    Wiring harnesses were made

    Three Fadecandy boards and a USB camera are connected to an Intel NUC running ubuntu.

    The NUC runs the fadecandy server, and several different python scripts which drive
    different applications on the board.

    I SSH into the nuc to run different programs, or run them from the OpenGL server locally,
    when I'm away from the device.


For the most part, I focused on things you could buy from hobbiest stores, with
good documentation and readily available.
    Adafruit
    SparkFun
    Amazon

The notable exceptions are the power supply, the connectors and the breakout boards.

Good Power supplies aren't cheap, and if they break, they can have the sort of catastrophic
failures associated with evil villans. Be careful, don't burn your house down.

Semiconductors, and many sensors are sort of electrically fragile. They need quality
power supplies with specific characteristics to run well. There are a variety of
ways to get into the bounds of what most require, and they have their tradeoffs which
are really better left to another talk, or more likely just a textbook. Typically I
determine my power requirements, and then pick the meanwell power supply from the
Jameco catalog which fits the bounds.

Soldering everything together is a bad idea. It's hard to prototype, hard to test,
and it's hard to maintain, and it's fragile. Solder is not load bearing. Wires are not
load bearing, shipping is risky. This is why I got the breakout boards and connectors.

The breakout board I had custom built was more for my own convenience than anything.
    Designed for free with Eagle (free)
    Built for cheap by OSHPark.
    I'm selling them on tindie ($1.5)

Ok great! Back to Software!

The first thing I did was display some basic images on four boards, connecting
one fade candy, four neopixel arrays, a benchtop power supply, and my laptop.

This stretched a number of areas:
    Python Image Library manipulation
    Python Program -> Fadecandy server -> Fadecandy Board -> Neopixel connection
    Image mapping to board layout

Then I got gifs running on the prototype hardware:
    PIL -> GIF Frame -> Previous Setup
    This way I could test moving pictures and framerate

Then I got SimpleCV setup.
    I still don't have SimpleCV running with my laptop.
    Turn the camera image into something that I can feed to the display.
    First step to live image manipulation.

Then I started fiddling with what I can do with OpenCV.
    Face Detection?
        It's not good enough (at least with my camera?) to detect faces in real time
    Motion Detection?
        This works
    Image Manipulation?
        This works.

I promised talking about networks a bit, so I built tetris.
    Or rather, I borrowed a pygame implementation of tetris, and rewrote all the control and display methods.
    It's now controlled from a redis queue, and displays to the mirror.

    I can connect from my phone and use it as the controller.

    In fact... we can all connect from our phones and use them as the controller.
    A flask-socketio server (https://naith.local:5000) means we can play tetris together!

Thanks for coming!

If you want to see any of the code, it's online ____
If you want to see the piece, I'm going to move it back to the open space.

--- Open It up ---
What bits would you like more of an explanation on?

