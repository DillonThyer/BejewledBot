#A simple bot made in python to play Bejewled 3 lighting mode on steam

#DEPENDANCIES:
# autopy library
# PIL (python imaging library)

#NOTE: must be run as an admin to allow autopy
#to move and click using the cursor.


#It will attempt to play whenever it sees what "looks" like a valid bejewled
#board, so don't let it "play" your desktop, been there done that.
#stopping it is a bit hard (need a better stop clause), starting it is easy.
#I am still new to python, so it is not the neatest.

#The "BOARD" is reffering to the 8x8 grid of gems

#Author: Dillon Thyer

import autopy as ap
import sys
import time
import win32gui

#TODO DRIVERS ONCE POLISHED
#quick start and stop keys

#Global constants
SLEEP_TIME = 0.02
BOARD = [[0 for col in range (0,8)]for row in range(0,8)]

#Max moves to be qued, changing this effects performance,
#lower -> higher chance of geting stuck, higher -> slower
#as more redundant moves are made, you can change this.
#I reccomend 5-10 as the max in most cases
MAX = 10
moves = 0

#WINDOW FUNCTIONS, normalising mouse positions

#getwindow, sets the current window as 500 by 500 in top left corner
#called on initial setup, you want the current window to be the bejewled window
def setupWindow():
    print "CLICK BEJEWLED WINDOW"
    time.sleep(5)
    bwindow = win32gui.GetForegroundWindow()
    win32gui.MoveWindow(bwindow, 0, 0, 500, 500, True)
           

#COLOR RECOGNITION FUNCTIONS

#"BLANK" means that the gem is not recognised as any of the
# defined gem colors Red,Blue,White,Yellow,Orange,Green,Purple
def getCol(r,g,b):
    if (r>=200 and g>=30 and g<=70 and b>=50 and b<=110):
        return "R"
    if (r>=0 and r<=80 and g>=100 and g<=220 and b>=200):
        return "B"
    if (r>=240 and g>=240 and b>=240):
        return "W"
    if (r>=230 and g>=170 and g<=255 and b>=10 and b<=90):
        return "Y"
    if (r>=240 and g>=215 and b>=100 and b<=150):
        return "O"
    if (r>=60 and r<=110 and g>=245 and b>=100 and b<=150):
        return "G"
    if (r>=130 and r<=255 and g>=0 and b>=120 and b<=255):
        return "P"
    else:
        return "BLANK"

#MOUSE FUNCTIONS
def leftClick():
    ap.mouse.toggle(True,ap.mouse.LEFT_BUTTON)
    time.sleep(SLEEP_TIME)

def releaseLeft():
    ap.mouse.toggle(False,ap.mouse.LEFT_BUTTON)
    time.sleep(SLEEP_TIME)

def moveMouse(x,y):
    ap.mouse.move(x,y)
    time.sleep(SLEEP_TIME)

def click(x,y):
    moveMouse(x,y)
    leftClick()
    releaseLeft()

#BOARD FUNCTIONS

#Maps 0..7 in 8x8 grid co-ordinates to return the real 
#screen co-ordinates for use with mouse functions.
def mapMove(x,y):
    xOff = 234.375
    yOff = 95.5
    realX = xOff + (x*48.75)
    realY = yOff + (y*49)
    return (int(realX),int(realY))

#Takes a screenshot of the board and grabs the RGB values
#of each gem, feeds them to color recognition function getCol
#then puts 
def getBoard():
    import PIL.ImageGrab
    im = PIL.ImageGrab.grab(bbox=(0,0,640,510))
    for i in range (0,8):
        for j in range (0,8):
            x,y = mapMove(j,i)
            r,g,b = im.load()[x,y]
            BOARD[i][j] = getCol(r,g,b)

#Checks wether the gems at 2 positions are the same color
def same(x1,y1,x2,y2):
    #check positions passed are in the 8x8 grid
    if (x1<0 or x1>7 or y1<0 or y1>7 or x2<0 or x2>7 or y2<0 or y2>7):
        return False
    if (BOARD[y1][x1] == BOARD[y2][x2]):
        return True

#moves a gem from (x1,y1) to (x2,y2)
def move(x1,y1,x2,y2):
    global moves
    startX,startY = mapMove(x1,y1)
    moveMouse(startX,startY)
    leftClick()
    endX,endY = mapMove(x2,y2)
    moveMouse(endX,endY)
    releaseLeft()
    moves = moves + 1

#Crude function to determine if a game has started,
#the menus are mainly purple, so if we see enough non-blank 
#spots and not too many purple, the game must have started.
#measure to prevent the bot "playing" your desktop.
def started():
    count = 0
    countp = 0
    for y in range(0,8):
        for x in range(0,8):
            if (BOARD[y][x]=="BLANK"):
                count = count + 1
            if (BOARD[y][x]=="P"):
                countp = countp + 1
    if (countp >= 25):
        return False
    if (count <= 20):
        return True
    return False

#MAIN
def main():
    #initialisation/setup
    global MAX
    global moves
    setupWindow()
    time.sleep(5)

    while True:
        #update the board info constantly
        getBoard()

        #if a game has started
        if (started()):
            #get the board info
            moves = 0
            getBoard()
            #for every tile in the board
            for y in range (0,8):
                #if we have tried more moves than allowed in the que
                #break and get the board info again
                if (moves > MAX):
                    break
                for x in range (0,8):
                    #Algorithm to find matches 5 big cases (UGLY)
                    #Looks at where matches could be given 2 gems of the same color next to each other
                    #for the majority of cases.

                    #gem above current is same color
                    if same(x,y,x,y-1):
                        if same(x,y,x-1,y-2): move(x-1,y-2,x,y-2)
                        if same(x,y,x+1,y-2): move(x+1,y-2,x,y-2)
                        if same(x,y,x,y-3): move (x,y-3,x,y-2)
                    #gem below current is same color
                    if same(x,y,x,y+1):
                        if same(x,y,x-1,y+2): move(x-1,y+2,x,y+2)
                        if same(x,y,x+1,y+2): move(x+1,y+2,x,y+2)
                        if same(x,y,x,y+3): move(x,y+3,x,y+2)
                    #gem left of current is same color
                    if same(x,y,x-1,y):
                        if same(x,y,x-3,y): move(x-3,y,x-2,y)
                        if same(x,y,x-2,y-1): move(x-2,y-1,x-2,y)
                        if same(x,y,x-2,y+1): move(x-2,y+1,x-2,y)
                    #gem right of current is same color
                    if same(x,y,x+1,y):
                        if same(x,y,x+3,y): move(x+3,y,x+2,y)
                        if same(x,y,x+2,y-1): move(x+2,y-1,x+2,y)
                        if same(x,y,x+2,y+1): move(x+2,y+1,x+2,y)
                    #holes vertical
                    if same(x,y,x,y+2):
                        if same(x,y,x-1,y+1): move(x-1,y+1,x,y+1)
                        if same(x,y,x+1,y+1): move(x+1,y+1,x,y+1)
                    #holes horizontal
                    if same(x,y,x+2,y):
                        if same(x,y,x+1,y-1): move(x+1,y-1,x+1,y)
                        if same(x,y,x+1,y+1): move(x+1,y+1,x+1,y)
#call main
main()
