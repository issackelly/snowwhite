#Snow White Part 2: Driving LEDs with Python

I'm writing about an interactive art piece I brough to PyOhio and how I built it.

Josh Boles got a (picture)[https://twitter.com/joshboles/status/493466700684091392/photo/1] I like, of the piece while I was talking about something else and the room was playing tetris (More on that soon!)

This post is about the image manipulation.

The piece I built had 20 of the 8 by 8 NeoPixel Matrices to make a canvas. It was arranged like so:


    [ 0] [ 1] [ 2] [ 3]
    [ 4] [ 5] [ 6] [ 7]
    [ 8] [ 9] [10] [11]
    [12] [13] [14] [15]
    [16] [17] [18] [19]

So, Four columns, and 5 rows. 20 different individual matrices. Each one had 64 LEDs in it's own matrix, represented to the underlying hardware as a list of LEDs, each with three color values (more in the last post)

In the last post, I showed how to get the pixel values out of an 8 by 8 image and then how to send those out to a single channel of a single fadecandy board.

This time, I'm just going to cover working with an image, or a series of images (animated gifs) to get it to the right format and dimensions.

PIL and/or Pillow are the standard for image manipulation with python. It's actually incredibly easy.

In my code, I kept a config file (utils.py) of sorts with the dimensions of the LED array (32 pixels by 40 pixels) and how the layout of the overall piece was represented as a single string of LEDs.

The layout variable was a list of 2-tuples representing the edges of a square within the array. The first was 0,0 to 7,7, The Second (matrix 1) was 8, 0 to 15, 7, moving all the way to #19 representing pixels 24, 32 to 31, 39.

To say this another way, I have a list of the top left and bottom right pixels of every individual matrix of LEDs. Then I match that up to an image of the same size as my array, and I get  every pixel of that image and put it at the right spot in my list. Then I display the image.

Let's start with opening an image and resizing it to fit the piece. Most images aren't meant to be displayed at 32 by 40, but we'll go with it anyway.

I adapted this code from the sorl-thumbnail package, which did the thing I wanted already. Don't rewrite code if somebody else does the thing you want already unless you have a good reason.

The following code will fit an image to the desired "size", and will crop to the center.

    from PIL import  Image
    size = (32, 40)
    img = Image.open('~/path/to/image.jpg')

    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
                Image.ANTIALIAS)
        # Crop middle
        box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
                Image.ANTIALIAS)
        # Crop in the middle
        box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
        img = img.crop(box)
    else :
        img = img.resize((size[0], size[1]), Image.ANTIALIAS)
        # If the scale is the same, we do not need to crop

First you compare the ratios of the image and the desired size, then you crop them to the same ratio.

After that, a resize operation brings it to the right dimensions.

Animated gifs or videos basically repeat the same proceess once for every frame. Due to compression optimizations, it's a little more complicated than that, but it's basically the same.


