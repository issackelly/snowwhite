import svgwrite

cut_rad = 1.4

board = {
    "width": 71.5,
    "height": 71.5,
    "quad_cuts": [
        # [x, y, w, h]
        ### -- [0.3, 7, 8.5, 3.8]
    ],
    "circle_cuts": [
        #[start_x, start_y, radius] ... needs to be adjusted to cx cy by adding
        # the radius to start_x and start_y, but start is the easier way to measure
        #
        #[1.5, 16.35, cut_rad],
        ### -- [1.5, 34.17, cut_rad],
        ### -- [1.5, 51.92, cut_rad],
### --
        ### -- [25.32, 7.51, cut_rad],
        ### -- [25.32, 34.22, cut_rad],
        ### -- [25.32, 60.82, cut_rad],
### --
### --
        ### -- [43.17, 7.51, cut_rad],
        ### -- [43.17, 34.22, cut_rad],
        ### -- [43.17, 60.82, cut_rad],
### --
        ### -- [67.13, 16.35, cut_rad],
        ### -- [67.13, 34.17, cut_rad],
        ### -- [67.13, 51.92, cut_rad],

        # Extras
        [14, 20, cut_rad],
        [14, 50, cut_rad],
        [34, 20, cut_rad],
        [34, 50, cut_rad],
        [55, 20, cut_rad],
        [55, 50, cut_rad],
        [-2, -5, 3 * cut_rad],
        [-2, 15, 3 * cut_rad],
    ],
    "text": [
        # x, y, size, rotation, text
        [0.5,15,8,270,"d"],
        [3.5,15,8,270,"+"],
        [6.5,15,8,270,"-"],
    ],
    "spacing": 1,
}

def _p(*args):
    """
    MM spacing for a png, for a single or group of numbers
    """
    ret = [mm * svgwrite.mm for mm in args ]
    if len(ret) == 1:
        return ret[0]
    return ret

def add_board(dwg, pos, x=None, y=None, index=None):
    """
    This command adds a board to dwg at position pos.
    """
    #dwg.add(
    #    dwg.rect(
    #        _p(*pos[:2]),
    #        _p(board["width"], board["height"]),
    #        stroke_width=2,
    #        stroke='blue',
    #        fill="none"
    #    )
    #)

    for cut in board["quad_cuts"]:
        cut_x = _p(pos[0] + cut[0])
        cut_y = _p(pos[1] + cut[1])

        dwg.add(dwg.rect(
            (cut_x, cut_y),
            _p(cut[2], cut[3]),
            stroke_width=CUT,
            stroke='green',
            fill="none"
        ))

    for cut in board["circle_cuts"]:
        cut_cx = _p(pos[0] + cut[0] + cut[2])
        cut_cy = _p(pos[1] + cut[1] + cut[2])

        dwg.add(dwg.circle(
            (cut_cx, cut_cy),
            _p(cut[2]),
            stroke_width=CUT,
            stroke='green',
            fill="none"
        ))

    for text in board["text"]:
        t_x = _p(pos[0] + text[0])
        t_y = _p(pos[1] + text[1])

        dwg.add(dwg.text(
            text[4],
            insert=(t_x, t_y),
            #rotate=[text[3]],
            style="font-size:8px;font-family:Open Sans;font-weight:bold;stroke:blue;stroke-width:1;fill:blue"
        ))

    t_x = _p(pos[0] + (board["width"] / 3) )
    t_y = _p(pos[1] + (board["height"] / 3) + 5)

    dwg.add(dwg.text(
        "%s (%s, %s)" % (index, x, y),
        insert=(t_x, t_y),
        #rotate=[text[3]],
        style="font-size:15px;font-family:Open Sans;font-weight:bold;stroke:blue;stroke-width:1;fill:blue"
    ))



ACRYLIC_THICKNESS = 3.175
HEIGHT_FROM_FRAME = 40
CUT = .0254 * svgwrite.mm # This is the "stroke" of the cut which signals to the epilog to
           # cut all the way through and not to rasterize it.
#CUT = 1 # for viewing

origin = 2, 2 # Origin of cutting tool, will make up for unsquare placement in laser up to this amount.
margin = 5.5, 6.75 # From outside of acrylic to first piece

size = 300,375 # - (2 * ACRYLIC_THICKNESS)# of the backing board

layout = 4, 5 # Array of neopixel boards



boards = []
i = 0
j = 0
k = 0
while j < layout[1]:
    while i < layout[0]:
        boards.append(
            (
                (board["width"] + board["spacing"]) * i + margin[0] + origin[0],
                (board["height"] + board["spacing"]) * j + margin[1] + origin[0],
                i,
                j,
                k,
            )
        )
        i+=1
        k+=1
    i=0
    j+=1

dwg = svgwrite.Drawing('board.svg', size=_p(457, 609.6), profile='full')

#gray background
#dwg.add(dwg.rect(_p(0,0), _p(457, 609.6), stroke_width=0, fill="rgb(222,222,222)"))

# Primary Backplane
# dwg.add(dwg.rect(_p(*origin), _p(*size), stroke_width=CUT, stroke='red', fill="none"))


# top/bottom are == side length - 2x thickness
# dwg.add(dwg.rect(_p(2, 377), _p(300, HEIGHT_FROM_FRAME), stroke_width=CUT, stroke='red', fill="none"))
# dwg.add(dwg.rect(_p(2, 377 + HEIGHT_FROM_FRAME), _p(300, HEIGHT_FROM_FRAME), stroke_width=CUT, stroke='red', fill="none"))
#
# dwg.add(dwg.rect(_p(302, 2), _p(HEIGHT_FROM_FRAME, 375 - (2 * ACRYLIC_THICKNESS)), stroke_width=CUT, stroke='red', fill="none"))
# dwg.add(dwg.rect(_p(302 + HEIGHT_FROM_FRAME, 2), _p(HEIGHT_FROM_FRAME, 375 - (2 * ACRYLIC_THICKNESS)), stroke_width=CUT, stroke='red', fill="none"))


for b_pos in boards:
    add_board(dwg, b_pos[:2], *b_pos[2:])


dwg.save()
