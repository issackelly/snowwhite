#!/usr/bin/env python

# Open Pixel Array Tetris, Issac Kelly, 2014
#
# Originally based on the following:
#
# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, redis
import opc, sys
from PIL import  Image, ImageDraw
from utils import pil_resize_crop, layout, size

r = redis.Redis()

BLOCK_SIZE = 2

BOARDWIDTH = int(size[0]/BLOCK_SIZE)

BOARDHEIGHT = int(size[1]/BLOCK_SIZE)

BLANK = '.'

WINDOWWIDTH = size[0]
WINDOWHEIGHT = size[1]

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BLOCK_SIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BLOCK_SIZE) - 2



MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1


COLORS  = (
    (102, 51, 153),
    (79, 47, 113),
    (82, 35, 53),
    (70, 30, 56),
    (182, 162, 197),
)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while r.get('stop_pattern') == 'No': # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over

        # Pull an Action from the redis queue
        #action = redis.lpop('action', None)
        action = r.lpop('tetris')

        if action == 'l' and isValidPosition(board, fallingPiece, adjX=-1):
            fallingPiece['x'] -= 1
            movingLeft = True
            movingRight = False
            lastMoveSidewaysTime = time.time()

        elif action == 'r' and isValidPosition(board, fallingPiece, adjX=1):
            fallingPiece['x'] += 1
            movingRight = True
            movingLeft = False
            lastMoveSidewaysTime = time.time()

        else:
            movingRight = False
            movingLeft = False

        # rotating the piece (if there is room to rotate)
        if action == 'x':
            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
            if not isValidPosition(board, fallingPiece):
                fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])

        if action == '+': # rotate the other direction
            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
            if not isValidPosition(board, fallingPiece):
                fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])



        ###        # making the piece fall faster with the down key
        ###        elif (event.key == K_DOWN or event.key == K_s):
        ###            movingDown = True
        ###            if isValidPosition(board, fallingPiece, adjY=1):
        ###                fallingPiece['y'] += 1
        ###            lastMoveDownTime = time.time()

        # move the current piece all the way down
        if action == 'd':
            movingDown = False
            movingLeft = False
            movingRight = False
            for i in range(1, BOARDHEIGHT):
                if not isValidPosition(board, fallingPiece, adjY=i):
                    break
            fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen

        im = Image.new("RGB", size, "black")
        draw = ImageDraw.Draw(im)
        draw.rectangle((0,0,0,0), "white")

        im, draw = drawBoard(board, im, draw)
        if fallingPiece != None:
            im, draw = drawPiece(fallingPiece, im, draw)

        # OPC Frame
        frame = []
        for start, end in layout:
            i = start[0]
            j = start[1]
            while j <= end[1]:
                while i <= end[0]:
                    frame.append(im.getpixel((i,j))[:3]) # Only want RGB, not RGBA
                    i+=1
                j+=1
                i = start[0]
        client.put_pixels(frame)



def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved

def drawBox(x, y, color, im, draw):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return

    draw.rectangle(
        (x*BLOCK_SIZE, y*BLOCK_SIZE,
        x*BLOCK_SIZE + BLOCK_SIZE - 1, y*BLOCK_SIZE + BLOCK_SIZE - 1),
    COLORS[color])

    return im, draw


def drawBoard(board, im, draw):
    # draw the individual boxes on the board

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                continue
            else:
                draw.rectangle(
                    (x*BLOCK_SIZE, y*BLOCK_SIZE,
                    x*BLOCK_SIZE + BLOCK_SIZE - 1, y*BLOCK_SIZE + BLOCK_SIZE - 1),
                COLORS[board[x][y]])
    return im, draw


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BLOCK_SIZE)), (TOPMARGIN + (boxy * BLOCK_SIZE))



def drawPiece(piece, im, draw):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]

    pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                bx = pixelx + (x * BLOCK_SIZE)
                by = pixely + (y * BLOCK_SIZE)

                draw.rectangle(
                    (
                        (bx, by),
                        (bx + BLOCK_SIZE - 1, by + BLOCK_SIZE - 1)
                    ), COLORS[piece['color']])

    return im, draw


def main():
    global client

    black = [ (0,0,0) ] * size[0] * size[1]
    client.put_pixels(black)

    # Clear the event queue
    r.delete('tetris')

    while r.get('stop_pattern') == 'No': # game loop
        runGame()
        # gameover
        r.delete('tetris')


from base import Pattern

class Tetris(Pattern):

    def run(self, **kwargs):
        global client
        client = self.client

        # reset game
        self.redis_client.delete('tetris')

        while self.redis_client.get('stop_pattern') == 'No': # game loop
            runGame()
            # gameover
            self.redis_client.delete('tetris')

if __name__ == '__main__':
    client = opc.Client('localhost:7890')
    r.set('stop_pattern', 'No')
    main()
