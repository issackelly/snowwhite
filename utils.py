from PIL import Image

size = 32, 40

layout = (
    ([0,0], [7,7]),
    [[8,0], [15,7]],
    ([16,0], [23,7]),
    ([24,0], [31,7]),

    ([0,8], [7,15]),
    [[8,8], [15,15]],
    ([16,8], [23,15]),
    ([24,8], [31,15]),

    ([0,16], [7,23]),
    [[8,16], [15,23]],
    ([16,16], [23,23]),
    ([24,16], [31,23]),

    ([0,24], [7,31]),
    [[8,24], [15,31]],
    ([16,24], [23,31]),
    ([24,24], [31,31]),

    ([0,32], [7,39]),
    [[8,32], [15,39]],
    ([16,32], [23,39]),
    ([24,32], [31,39]),
)


def pil_resize_crop(img, size):
    """
    Resize and crop an image to fit the specified size.

    args:
        img_path: path for the image to resize.
        modified_path: path to store the modified image.
        size: `(width, height)` tuple.
        crop_type: can be 'top', 'middle' or 'bottom', depending on this
            value, the image will cropped getting the 'top/left', 'midle' or
            'bottom/rigth' of the image to fit the size.
    raises:
        Exception: if can not open the file in img_path of there is problems
            to save the image.
        ValueError: if an invalid `crop_type` is provided.
    """

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
        img = img.resize((size[0], size[1]),
                Image.ANTIALIAS)
        # If the scale is the same, we do not need to crop

    return img



def simplecv_smart_crop(im, final_size):
    final_scale = final_size[0] / float(final_size[1])
    orig_scale = im.width / float(im.height)


    if final_scale > orig_scale: # take the width at 100%
        crop = [
            0,
            (im.height - (im.width / final_scale) ) / 2,
            im.width,
            im.width / final_scale
        ]

    elif final_scale < orig_scale:
        crop = [
            (im.width - (im.height * final_scale) )/ 2,
            0,
            im.height * final_scale,
            im.height
        ]

    else:
        return im

    return im.crop(crop)

