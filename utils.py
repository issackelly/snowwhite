

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

