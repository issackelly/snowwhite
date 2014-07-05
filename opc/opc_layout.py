layout = []

ONE_BOARD = [
    {"point": [0, 0, 0]},
    {"point": [1, 0, 0]},
    {"point": [2, 0, 0]},
    {"point": [3, 0, 0]},
    {"point": [4, 0, 0]},
    {"point": [5, 0, 0]},
    {"point": [6, 0, 0]},
    {"point": [7, 0, 0]},

    {"point": [0, 1, 0]},
    {"point": [1, 1, 0]},
    {"point": [2, 1, 0]},
    {"point": [3, 1, 0]},
    {"point": [4, 1, 0]},
    {"point": [5, 1, 0]},
    {"point": [6, 1, 0]},
    {"point": [7, 1, 0]},

    {"point": [0, 2, 0]},
    {"point": [1, 2, 0]},
    {"point": [2, 2, 0]},
    {"point": [3, 2, 0]},
    {"point": [4, 2, 0]},
    {"point": [5, 2, 0]},
    {"point": [6, 2, 0]},
    {"point": [7, 2, 0]},

    {"point": [0, 3, 0]},
    {"point": [1, 3, 0]},
    {"point": [2, 3, 0]},
    {"point": [3, 3, 0]},
    {"point": [4, 3, 0]},
    {"point": [5, 3, 0]},
    {"point": [6, 3, 0]},
    {"point": [7, 3, 0]},

    {"point": [0, 4, 0]},
    {"point": [1, 4, 0]},
    {"point": [2, 4, 0]},
    {"point": [3, 4, 0]},
    {"point": [4, 4, 0]},
    {"point": [5, 4, 0]},
    {"point": [6, 4, 0]},
    {"point": [7, 4, 0]},

    {"point": [0, 5, 0]},
    {"point": [1, 5, 0]},
    {"point": [2, 5, 0]},
    {"point": [3, 5, 0]},
    {"point": [4, 5, 0]},
    {"point": [5, 5, 0]},
    {"point": [6, 5, 0]},
    {"point": [7, 5, 0]},

    {"point": [0, 6, 0]},
    {"point": [1, 6, 0]},
    {"point": [2, 6, 0]},
    {"point": [3, 6, 0]},
    {"point": [4, 6, 0]},
    {"point": [5, 6, 0]},
    {"point": [6, 6, 0]},
    {"point": [7, 6, 0]},

    {"point": [0, 7, 0]},
    {"point": [1, 7, 0]},
    {"point": [2, 7, 0]},
    {"point": [3, 7, 0]},
    {"point": [4, 7, 0]},
    {"point": [5, 7, 0]},
    {"point": [6, 7, 0]},
    {"point": [7, 7, 0]},
]

## Spatially laying out these arrays in the way that they'll be on the board.
basic = [
    0,   1,  2,  3,
    4,   5,  6,  7,
    8,   9, 10, 11,
    12, 13, 14, 15,
    16, 17, 18, 19
]

# Each X/Y offset for any individual BOARD
offset = [
    [-2,-2], [-1, -2], [0, -2], [1, -2],
    [-2,-1], [-1, -1], [0, -1], [1, -1],
    [-2, 0], [-1, 0], [0, 0], [1, 0],
    [-2, 1], [-1, 1], [0, 1], [1, 1],
    [-2, 2], [-1, 2], [0, 2], [1, 2]
]


for i in basic:
    for point_obj in ONE_BOARD:
        layout.append({
            "point": [
                (offset[i][0] * 8) + point_obj["point"][0], # X is 8 wide
                (offset[i][1] * 8) + point_obj["point"][1], # Y is 8 wide
                0
            ]
        })

import json
print json.dumps(layout)
