#########################################################################
# REAME!
#
# This program is based on a program made by Al Swaigart:
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
#
# modified by Willem Vermeeren
#
# You're able to add walls and enable and disable AI by changing the first 3 variables
#
# HF!
#########################################################################


AIred = True
AIblue = True    
addWalls = 10    # amount of walls you want (I recommend not going over 10 but you do you)

FPS = 20     # change the speed of the snakes
WINDOWWIDTH = 1290
WINDOWHEIGHT = 630
CELLSIZE = 30


import random, pygame, sys
from pygame.locals import *
import math
import time

up2Key = K_UP
down2Key = K_DOWN
left2Key = K_LEFT
right2Key = K_RIGHT

up1Key = K_z
down1Key = K_s
left1Key = K_q
right1Key = K_d


MENUICONSIZE = 200
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

gameoverPadding = [40, 10, 40, 10]

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
BLUE      = (  0,   0, 155)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 60,  60,  60)
GRAY      = (100, 100, 100)


bgGreen1 = (80, 200, 2)
bgGreen2 = (70, 180, 2)

BGCOLOR = BLACK



menuElements = {
    "IconB": pygame.transform.scale(pygame.image.load('assets/menuElements/blue.png'), (MENUICONSIZE, MENUICONSIZE)),
    "IconR": pygame.transform.scale(pygame.image.load('assets/menuElements/red.png'), (MENUICONSIZE, MENUICONSIZE)),
}

appleImage = pygame.transform.scale(pygame.image.load('assets/apple.png'), (CELLSIZE, CELLSIZE))

worm1sprite = {
    "straight":{
        "horizontal": pygame.transform.scale(pygame.image.load('assets/worm1/straight/horizontal.png'), (CELLSIZE, CELLSIZE)),
        "vertical": pygame.transform.scale(pygame.image.load('assets/worm1/straight/vertical.png'), (CELLSIZE, CELLSIZE))
    },
    "angle":{
        "BL": pygame.transform.scale(pygame.image.load('assets/worm1/angle/BL.png'), (CELLSIZE, CELLSIZE)),
        "LU": pygame.transform.scale(pygame.image.load('assets/worm1/angle/LU.png'), (CELLSIZE, CELLSIZE)), # loads all images in array
        "BR": pygame.transform.scale(pygame.image.load('assets/worm1/angle/RB.png'), (CELLSIZE, CELLSIZE)),
        "UR": pygame.transform.scale(pygame.image.load('assets/worm1/angle/UR.png'), (CELLSIZE, CELLSIZE))
    },
    "head":{
        "U": pygame.transform.scale(pygame.image.load('assets/worm1/head/U.png'), (CELLSIZE, CELLSIZE)),
        "L": pygame.transform.scale(pygame.image.load('assets/worm1/head/L.png'), (CELLSIZE, CELLSIZE)),
        "D": pygame.transform.scale(pygame.image.load('assets/worm1/head/D.png'), (CELLSIZE, CELLSIZE)),
        "R": pygame.transform.scale(pygame.image.load('assets/worm1/head/R.png'), (CELLSIZE, CELLSIZE))
    },
    "tail":{
        "U": pygame.transform.scale(pygame.image.load('assets/worm1/tail/U.png'), (CELLSIZE, CELLSIZE)),
        "L": pygame.transform.scale(pygame.image.load('assets/worm1/tail/L.png'), (CELLSIZE, CELLSIZE)),
        "D": pygame.transform.scale(pygame.image.load('assets/worm1/tail/D.png'), (CELLSIZE, CELLSIZE)),
        "R": pygame.transform.scale(pygame.image.load('assets/worm1/tail/R.png'), (CELLSIZE, CELLSIZE))
    }
}

worm2sprite = {
    "straight":{
        "horizontal": pygame.transform.scale(pygame.image.load('assets/worm2/straight/horizontal.png'), (CELLSIZE, CELLSIZE)),
        "vertical": pygame.transform.scale(pygame.image.load('assets/worm2/straight/vertical.png'), (CELLSIZE, CELLSIZE))
    },
    "angle":{
        "BL": pygame.transform.scale(pygame.image.load('assets/worm2/angle/BL.png'), (CELLSIZE, CELLSIZE)),
        "LU": pygame.transform.scale(pygame.image.load('assets/worm2/angle/LU.png'), (CELLSIZE, CELLSIZE)), # loads all images in array
        "BR": pygame.transform.scale(pygame.image.load('assets/worm2/angle/RB.png'), (CELLSIZE, CELLSIZE)),
        "UR": pygame.transform.scale(pygame.image.load('assets/worm2/angle/UR.png'), (CELLSIZE, CELLSIZE))
    },
    "head":{
        "U": pygame.transform.scale(pygame.image.load('assets/worm2/head/U.png'), (CELLSIZE, CELLSIZE)),
        "L": pygame.transform.scale(pygame.image.load('assets/worm2/head/L.png'), (CELLSIZE, CELLSIZE)),
        "D": pygame.transform.scale(pygame.image.load('assets/worm2/head/D.png'), (CELLSIZE, CELLSIZE)),
        "R": pygame.transform.scale(pygame.image.load('assets/worm2/head/R.png'), (CELLSIZE, CELLSIZE))
    },
    "tail":{
        "U": pygame.transform.scale(pygame.image.load('assets/worm2/tail/U.png'), (CELLSIZE, CELLSIZE)),
        "L": pygame.transform.scale(pygame.image.load('assets/worm2/tail/L.png'), (CELLSIZE, CELLSIZE)),
        "D": pygame.transform.scale(pygame.image.load('assets/worm2/tail/D.png'), (CELLSIZE, CELLSIZE)),
        "R": pygame.transform.scale(pygame.image.load('assets/worm2/tail/R.png'), (CELLSIZE, CELLSIZE))
    }
}




UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

wormTAIL = "tail"
wormHEAD = "head"

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')


    while True:
        showStartScreen() #main loop
        data = runGame()
        showGameOverScreen(data)


def runGame():
    winner1 = False
    winner2 = False

    # Set a random start point.
    startx1 = 2
    starty1 = math.floor(CELLHEIGHT/2)
    worm1Coords = [{'x': startx1,     'y': starty1, "in":LEFT, "out":wormHEAD, "image":worm1sprite["head"]["R"]},
                  {'x': startx1 - 1, 'y': starty1, "in":LEFT, "out":RIGHT, "image":worm1sprite["straight"]["horizontal"]},
                  {'x': startx1 - 2, 'y': starty1, "in":wormTAIL, "out":RIGHT, "image":worm1sprite["tail"]["R"]}]

    direction1 = RIGHT #don't change this without changing the coords

    startx2 = CELLWIDTH-3
    starty2 = math.ceil(CELLHEIGHT/2)
    worm2Coords = [{'x': startx2,     'y': starty2, "in":RIGHT, "out":wormHEAD, "image":worm2sprite["head"]["L"]},
                  {'x': startx2 + 1, 'y': starty2, "in":RIGHT, "out":LEFT, "image":worm2sprite["straight"]["horizontal"]},
                  {'x': startx2 + 2, 'y': starty2, "in":RIGHT, "out":wormTAIL, "image":worm2sprite["tail"]["L"]}]

    direction2 = LEFT #don't change this without changing the coords

    walls = []

    if addWalls>0:
        for i in range(addWalls):
            dirs = [UP, DOWN, LEFT, RIGHT]
            length = random.randint(3, 7)               #creates walls that shouldn't kill the snake in start
            direction = dirs[random.randint(0, 3)]
            startCoords = getRandomLocation()
            walls.insert(0, [])
            
            for blockNr in range(length):
                if(direction==UP):
                    if not isOcupied({"x": startCoords["x"], "y": startCoords["y"]-blockNr}, worm1Coords, worm2Coords):
                        walls[0].insert(0, {"x": startCoords["x"], "y": startCoords["y"]-blockNr})
                elif(direction==DOWN):
                    if not isOcupied({"x": startCoords["x"], "y": startCoords["y"]+blockNr}, worm1Coords, worm2Coords):
                        walls[0].insert(0, {"x": startCoords["x"], "y": startCoords["y"]+blockNr})
                elif(direction==LEFT):
                    if not isOcupied({"x": startCoords["x"]-blockNr, "y": startCoords["y"]}, worm1Coords, worm2Coords):
                        walls[0].insert(0, {"x": startCoords["x"]-blockNr, "y": startCoords["y"]})
                elif(direction==RIGHT):
                    if not isOcupied({"x": startCoords["x"]+blockNr, "y": startCoords["y"]}, worm1Coords, worm2Coords):
                        walls[0].insert(0, {"x": startCoords["x"]+blockNr, "y": startCoords["y"]})
            
    

    # Start the apple in a random place.

    apple = placeNewApple(walls, worm1Coords, worm2Coords)
    apple2 = placeNewApple(walls, worm1Coords, worm2Coords)

    
    #--------stargin animation------------
    VSFont = pygame.font.Font('freesansbold.ttf', 150)
    drawGrid()
    drawWorm(worm1Coords)
    drawWorm(worm2Coords)
    #----- 3 -----
    drawWalls(walls)
    drawApple(apple)
    drawApple(apple2)
    drawScore1(len(worm1Coords) - 3)
    drawScore2(len(worm2Coords) - 3)
    VSSurf = VSFont.render('3', True, WHITE)
    VSRect = VSSurf.get_rect()
    VSRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/10+80)
    DISPLAYSURF.blit(VSSurf, VSRect)
    pygame.display.update()
    time.sleep(1)
    drawGrid()
    drawWorm(worm1Coords)
    drawWorm(worm2Coords)

    #----- /2 -----
    drawWalls(walls)
    drawApple(apple)
    drawApple(apple2)
    drawScore1(len(worm1Coords) - 3)
    drawScore2(len(worm2Coords) - 3)
    VSSurf = VSFont.render('2', True, WHITE)
    VSRect = VSSurf.get_rect()
    VSRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/10+80)
    DISPLAYSURF.blit(VSSurf, VSRect)
    pygame.display.update()
    time.sleep(1)
    drawGrid()
    drawWorm(worm1Coords)
    drawWorm(worm2Coords)

    #----- 1 -----
    drawWalls(walls)
    drawApple(apple)
    drawApple(apple2)
    drawScore1(len(worm1Coords) - 3)
    drawScore2(len(worm2Coords) - 3)
    VSSurf = VSFont.render('1', True, WHITE)
    VSRect = VSSurf.get_rect()
    VSRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/10+80)
    DISPLAYSURF.blit(VSSurf, VSRect)
    pygame.display.update()
    time.sleep(1)

    #----- start -----
    while True: # main game loop
        drawGrid()
        #--------------setting directions-------------------------
        newDirection1 = direction1 
        newDirection2 = direction2 #I work with a newdirection variable for preventing the snake to turn into their self when you turn to fast

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == left1Key) and direction1 != RIGHT and not AIblue:
                    newDirection1 = LEFT
                elif (event.key == right1Key) and direction1 != LEFT and not AIblue:
                    newDirection1 = RIGHT
                elif (event.key == up1Key) and direction1 != DOWN and not AIblue:
                    newDirection1 = UP
                elif (event.key == down1Key) and direction1 != UP and not AIblue:
                    newDirection1 = DOWN

                if (event.key == left2Key) and direction2 != RIGHT and not AIred:
                    newDirection2 = LEFT
                elif (event.key == right2Key) and direction2 != LEFT and not AIred:
                    newDirection2 = RIGHT
                elif (event.key == up2Key) and direction2 != DOWN and not AIred:
                    newDirection2 = UP
                elif (event.key == down2Key) and direction2 != UP and not AIred:
                    newDirection2 = DOWN

                elif event.key == K_ESCAPE:
                    terminate()

        if(AIred):
            newDirection2 = nextAiMove(worm2Coords, apple, apple2, worm1Coords, RED, walls) # here the AI gets to choose their new direction

        if(AIblue):
            newDirection1 = nextAiMove(worm1Coords, apple, apple2, worm2Coords, BLUE, walls)

        direction1 = newDirection1
        direction2 = newDirection2
        #--------------------apple eating----------------------------
    
        # check if worm has eaten an apply
        if worm1Coords[HEAD]['x'] == apple['x'] and worm1Coords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = placeNewApple(walls, worm1Coords, worm2Coords)

        elif worm1Coords[HEAD]['x'] == apple2['x'] and worm1Coords[HEAD]['y'] == apple2['y']:
            # don't remove worm's tail segment
            apple2 = placeNewApple(walls, worm1Coords, worm2Coords)
        else:
            del worm1Coords[-1] # remove worm's tail segment

        

        if worm2Coords[HEAD]['x'] == apple['x'] and worm2Coords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = placeNewApple(walls, worm1Coords, worm2Coords)
        elif worm2Coords[HEAD]['x'] == apple2['x'] and worm2Coords[HEAD]['y'] == apple2['y']:
            # don't remove worm's tail segment
            apple2 = placeNewApple(walls, worm1Coords, worm2Coords)
        else:
            del worm2Coords[-1] # remove worm's tail segment


        #-----------------worm 1 image calculation thingy------------------------
        
        # move the worm by adding a segment in the direction1 it is moving
        if direction1 == UP:
            newHead1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'] - 1, "in":DOWN, "out":wormHEAD, "image":worm1sprite["head"]["U"]} # sets in and out faces of snake
            newNeck1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'], "in":worm1Coords[HEAD]['in'], "out":UP} 
        elif direction1 == DOWN:
            newHead1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'] + 1, "in":UP, "out":wormHEAD, "image":worm1sprite["head"]["D"]}
            newNeck1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'], "in":worm1Coords[HEAD]['in'], "out":DOWN}

        elif direction1 == LEFT:
            newHead1 = {'x': worm1Coords[HEAD]['x'] - 1, 'y': worm1Coords[HEAD]['y'], "in":RIGHT, "out":wormHEAD, "image":worm1sprite["head"]["L"]}
            newNeck1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'], "in":worm1Coords[HEAD]['in'], "out":LEFT}

        elif direction1 == RIGHT:
            newHead1 = {'x': worm1Coords[HEAD]['x'] + 1, 'y': worm1Coords[HEAD]['y'], "in":LEFT, "out":wormHEAD, "image":worm1sprite["head"]["R"]}
            newNeck1 = {'x': worm1Coords[HEAD]['x'], 'y': worm1Coords[HEAD]['y'], "in":worm1Coords[HEAD]['in'], "out":RIGHT}
        

        if((newNeck1["in"]==LEFT or newNeck1["in"]==RIGHT) and (newNeck1["out"]==LEFT or newNeck1["out"]==RIGHT)): # horizontal         sets the neck ins and outs
            newNeck1["image"] = worm1sprite["straight"]["horizontal"]

        elif((newNeck1["in"]==UP or newNeck1["in"]==DOWN) and (newNeck1["out"]==UP or newNeck1["out"]==DOWN)):  #vertical
            newNeck1["image"] = worm1sprite["straight"]["vertical"]

        elif((newNeck1["in"]==UP or newNeck1["in"]==RIGHT) and (newNeck1["out"]==UP or newNeck1["out"]==RIGHT)):  #UR
            newNeck1["image"] = worm1sprite["angle"]["UR"]

        elif((newNeck1["in"]==DOWN or newNeck1["in"]==LEFT) and (newNeck1["out"]==DOWN or newNeck1["out"]==LEFT)):  #BL
            newNeck1["image"] = worm1sprite["angle"]["BL"]

        elif((newNeck1["in"]==LEFT or newNeck1["in"]==UP) and (newNeck1["out"]==LEFT or newNeck1["out"]==UP)):  #LU
            newNeck1["image"] = worm1sprite["angle"]["LU"]

        elif((newNeck1["in"]==DOWN or newNeck1["in"]==RIGHT) and (newNeck1["out"]==DOWN or newNeck1["out"]==RIGHT)):  #BR
            newNeck1["image"] = worm1sprite["angle"]["BR"]


        if(worm1Coords[len(worm1Coords)-1]["out"]==RIGHT):
            worm1Coords[len(worm1Coords)-1]["image"] = worm1sprite["tail"]["R"]       #sets the image of the tail depending on where the worm moves
        elif(worm1Coords[len(worm1Coords)-1]["out"]==LEFT):
            worm1Coords[len(worm1Coords)-1]["image"] = worm1sprite["tail"]["L"]
        elif(worm1Coords[len(worm1Coords)-1]["out"]==UP):
            worm1Coords[len(worm1Coords)-1]["image"] = worm1sprite["tail"]["U"]
        elif(worm1Coords[len(worm1Coords)-1]["out"]==DOWN):
            worm1Coords[len(worm1Coords)-1]["image"] = worm1sprite["tail"]["D"]
        
        worm1Coords[len(worm1Coords)-1]["in"] = wormTAIL  #sets the in side to tail
        
        
        worm1Coords.insert(0, newHead1)
        worm1Coords[1] = newNeck1
        #-----------------worm 2 image calculation thingy------------------------

        if direction2 == UP:
            newHead2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'] - 1, "in":DOWN, "out":wormHEAD, "image":worm2sprite["head"]["U"]} # sets in and out faces of snake
            newNeck2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'], "in":worm2Coords[HEAD]['in'], "out":UP} 
        elif direction2 == DOWN:
            newHead2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'] + 1, "in":UP, "out":wormHEAD, "image":worm2sprite["head"]["D"]}
            newNeck2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'], "in":worm2Coords[HEAD]['in'], "out":DOWN}

        elif direction2 == LEFT:
            newHead2 = {'x': worm2Coords[HEAD]['x'] - 1, 'y': worm2Coords[HEAD]['y'], "in":RIGHT, "out":wormHEAD, "image":worm2sprite["head"]["L"]}
            newNeck2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'], "in":worm2Coords[HEAD]['in'], "out":LEFT}

        elif direction2 == RIGHT:
            newHead2 = {'x': worm2Coords[HEAD]['x'] + 1, 'y': worm2Coords[HEAD]['y'], "in":LEFT, "out":wormHEAD, "image":worm2sprite["head"]["R"]}
            newNeck2 = {'x': worm2Coords[HEAD]['x'], 'y': worm2Coords[HEAD]['y'], "in":worm2Coords[HEAD]['in'], "out":RIGHT}
        

        if((newNeck2["in"]==LEFT or newNeck2["in"]==RIGHT) and (newNeck2["out"]==LEFT or newNeck2["out"]==RIGHT)): # horizontal         sets the neck ins and outs
            newNeck2["image"] = worm2sprite["straight"]["horizontal"]

        elif((newNeck2["in"]==UP or newNeck2["in"]==DOWN) and (newNeck2["out"]==UP or newNeck2["out"]==DOWN)):  #vertical
            newNeck2["image"] = worm2sprite["straight"]["vertical"]

        elif((newNeck2["in"]==UP or newNeck2["in"]==RIGHT) and (newNeck2["out"]==UP or newNeck2["out"]==RIGHT)):  #UR
            newNeck2["image"] = worm2sprite["angle"]["UR"]

        elif((newNeck2["in"]==DOWN or newNeck2["in"]==LEFT) and (newNeck2["out"]==DOWN or newNeck2["out"]==LEFT)):  #BL
            newNeck2["image"] = worm2sprite["angle"]["BL"]

        elif((newNeck2["in"]==LEFT or newNeck2["in"]==UP) and (newNeck2["out"]==LEFT or newNeck2["out"]==UP)):  #LU
            newNeck2["image"] = worm2sprite["angle"]["LU"]

        elif((newNeck2["in"]==DOWN or newNeck2["in"]==RIGHT) and (newNeck2["out"]==DOWN or newNeck2["out"]==RIGHT)):  #BR
            newNeck2["image"] = worm2sprite["angle"]["BR"]


        if(worm2Coords[len(worm2Coords)-1]["out"]==RIGHT):
            worm2Coords[len(worm2Coords)-1]["image"] = worm2sprite["tail"]["R"]       #sets the image of the tail depending on where the worm moves
        elif(worm2Coords[len(worm2Coords)-1]["out"]==LEFT):
            worm2Coords[len(worm2Coords)-1]["image"] = worm2sprite["tail"]["L"]
        elif(worm2Coords[len(worm2Coords)-1]["out"]==UP):
            worm2Coords[len(worm2Coords)-1]["image"] = worm2sprite["tail"]["U"]
        elif(worm2Coords[len(worm2Coords)-1]["out"]==DOWN):
            worm2Coords[len(worm2Coords)-1]["image"] = worm2sprite["tail"]["D"]
        
        worm2Coords[len(worm2Coords)-1]["in"] = wormTAIL  #sets the in side to tail
        
        
        worm2Coords.insert(0, newHead2)
        worm2Coords[1] = newNeck2
        #-----------------win conditions--------------------
        for wormBody in worm1Coords[1:]:
            if wormBody['x'] == worm1Coords[HEAD]['x'] and wormBody['y'] == worm1Coords[HEAD]['y']:
                winner2 = True 

            if wormBody['x'] == worm2Coords[HEAD]['x'] and wormBody['y'] == worm2Coords[HEAD]['y']: 
                winner1 = True

        

        for wormBody in worm2Coords[1:]:
            if wormBody['x'] == worm2Coords[HEAD]['x'] and wormBody['y'] == worm2Coords[HEAD]['y']:
                winner1 = True
                
            if wormBody['x'] == worm1Coords[HEAD]['x'] and wormBody['y'] == worm1Coords[HEAD]['y']:
                winner2 = True
                
        if inWall(walls, worm1Coords[HEAD]) and inWall(walls, worm2Coords[HEAD]):
            winner1 = True
            winner2 = True

        elif inWall(walls, worm2Coords[HEAD]):
            winner1 = True
        elif inWall(walls, worm1Coords[HEAD]):
            winner2 = True

        if(worm1Coords[HEAD]['x'] == worm2Coords[HEAD]['x'] and worm1Coords[HEAD]['y'] == worm2Coords[HEAD]['y']):
            winner2=True
            winner1=True

        if(winner1 and winner2):
            return {"winner": 0, "worm1Coords": worm1Coords, "worm2Coords": worm2Coords, "walls":walls} # worm 1 wins
        elif(winner1):
            return {"winner": 1, "worm1Coords": worm1Coords, "worm2Coords": worm2Coords, "walls":walls} # worm 1 wins
        elif(winner2):
            return {"winner": 2, "worm1Coords": worm1Coords, "worm2Coords": worm2Coords, "walls":walls} # worm 2 wins

        #-------------prevents snake from going of map-------------------------
        if worm1Coords[HEAD]['x'] == -1:
            worm1Coords[HEAD]['x'] = CELLWIDTH-1        #checks if they have gone of the map and teleports them to the other side
        elif worm1Coords[HEAD]['x'] == CELLWIDTH:
            worm1Coords[HEAD]['x'] = 0
        elif worm1Coords[HEAD]['y'] == -1:
            worm1Coords[HEAD]['y'] = CELLHEIGHT-1
        elif worm1Coords[HEAD]['y'] == CELLHEIGHT:
            worm1Coords[HEAD]['y'] = 0

        if worm2Coords[HEAD]['x'] == -1:
            worm2Coords[HEAD]['x'] = CELLWIDTH-1
        elif worm2Coords[HEAD]['x'] == CELLWIDTH:
            worm2Coords[HEAD]['x'] = 0
        elif worm2Coords[HEAD]['y'] == -1:
            worm2Coords[HEAD]['y'] = CELLHEIGHT-1
        elif worm2Coords[HEAD]['y'] == CELLHEIGHT:
            worm2Coords[HEAD]['y'] = 0
        #-------------drawing------------------------
        drawWorm(worm1Coords)
        drawWorm(worm2Coords)   #draws the screen
        drawWalls(walls)
        drawApple(apple)
        drawApple(apple2)
        drawScore1(len(worm1Coords) - 3)
        drawScore2(len(worm2Coords) - 3)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to restart.', False, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(menuElements["IconB"], (150, WINDOWHEIGHT/10))
    DISPLAYSURF.blit(menuElements["IconR"], (WINDOWWIDTH-150-MENUICONSIZE, WINDOWHEIGHT/10))  # draws startscreen

    playerFont = pygame.font.Font('freesansbold.ttf', 50)
    VSFont = pygame.font.Font('freesansbold.ttf', 150)

    player1Surf = playerFont.render('Player 1', True, WHITE)
    player1Rect = player1Surf.get_rect()
    player1Rect.topleft = (150, WINDOWHEIGHT/10+MENUICONSIZE+10)
    DISPLAYSURF.blit(player1Surf, player1Rect)

    player2Surf = playerFont.render('Player 2', True, WHITE)
    player2Rect = player2Surf.get_rect()
    player2Rect.topleft = (WINDOWWIDTH-150-MENUICONSIZE, WINDOWHEIGHT/10+MENUICONSIZE+10)
    DISPLAYSURF.blit(player2Surf, player2Rect)

    VSSurf = VSFont.render('VS', True, WHITE)
    VSRect = VSSurf.get_rect()
    VSRect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/10+80)
    DISPLAYSURF.blit(VSSurf, VSRect)

    while True:
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def checkForQuit():
    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT:
            terminate()

def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen(data):
    
    if(data["winner"]==1):
        gameOverMessage = "Blue wins"
        for i in range(6):
            drawGrid()
            drawWorm(data["worm1Coords"])
            if(i%2==0):
                drawWorm(data["worm2Coords"])
            drawWalls(data["walls"])
            drawScore1(len(data["worm1Coords"]) - 3) #gamover animation when 1 wins
            drawScore2(len(data["worm2Coords"]) - 3)
            pygame.display.update()
            checkForQuit()
            time.sleep(0.5)

    elif(data["winner"]==2):
        gameOverMessage = "Red wins"
        for i in range(6):
            drawGrid()
            drawWorm(data["worm2Coords"])
            if(i%2==0):
                drawWorm(data["worm1Coords"])

            drawWalls(data["walls"])
            drawScore1(len(data["worm1Coords"]) - 3)
            drawScore2(len(data["worm2Coords"]) - 3)    #gameover animation when 2 wins
            pygame.display.update()
            checkForQuit()
            time.sleep(0.5)
    else:
        gameOverMessage = "Tie"
        for i in range(6):
            drawGrid()
            if(i%2==0):
                drawWorm(data["worm2Coords"])   #gameover animation when tie
                drawWorm(data["worm1Coords"])

            drawWalls(data["walls"])
            pygame.display.update()
            checkForQuit()
            time.sleep(0.5)

    time.sleep(0.5)
    drawWalls(data["walls"])

    drawScore1(len(data["worm1Coords"]) - 3)
    drawScore2(len(data["worm2Coords"]) - 3)
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render(gameOverMessage, True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/2) #draws gameove screen

    DISPLAYSURF.blit(gameSurf, gameRect)
    drawPressKeyMsg()
    drawScore1(len(data["worm1Coords"]) - 3)
    drawScore2(len(data["worm2Coords"]) - 3)

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return


def drawScore1(score):
    scoreSurf = BASICFONT.render('Score blue : %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (0, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawScore2(score):
    scoreSurf = BASICFONT.render('Score red   : %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (0, 30)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for piece in wormCoords:
        x = piece['x'] * CELLSIZE
        y = piece['y'] * CELLSIZE
        DISPLAYSURF.blit(piece["image"], (x, y))

    

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    DISPLAYSURF.blit(appleImage, (x, y))



def drawGrid():
    pygame.draw.rect(DISPLAYSURF, bgGreen1, pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT))
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        for y in range(0, WINDOWHEIGHT, CELLSIZE):
            drawSquare(x, y)


def drawSquare(x, y):
    bgSquare = pygame.Rect(x, y, CELLSIZE, CELLSIZE) #I sperated it because I intent to make it faster by not always redrawing the entire screne every cycle
    if((x/CELLSIZE)%2+(y/CELLSIZE)%2==0 or (x/CELLSIZE)%2+(y/CELLSIZE)%2==2):
        pygame.draw.rect(DISPLAYSURF, bgGreen1, bgSquare)
    else:
        pygame.draw.rect(DISPLAYSURF, bgGreen2, bgSquare)



#------------------ AI stuff ----------------------------
def nextAiMove(AIwormCoords, apple1Coords, apple2Coords, OTwormCoords, color, walls):  #nice
    distScoreMultip = 1     #by making this number higher you make it have more impacht on the desicion making of the snake.
    BlockinPenalty = 100
    inHeadPenalty = 50
    notEnoughEscapeRoutesPenalty = 50

    minPosMoves = 20
    minEscapeRoutes = 2



    dirs = [UP, RIGHT, DOWN, LEFT]  # just the directions you can go in a list nothing more
    scores = [0, 0, 0, 0] #the scores in relation to the directions
    lowestScore = 100000000 #here comes the lowest score of the best move
    lowestScoreNr = -1  #the element in the direction list the snake should do    sentences 100

    ImportantNodes = [[], [], [], []] #nodes that have yet to be inspected
    VisitedNodes = [[], [], [], []]   #the nodes that have been found

    escapeRoutes = [0, 0, 0, 0]

    invalidDirection = AIwormCoords[HEAD]["in"]
    for dirNr in range(len(dirs)):
        if(dirs[dirNr]!=invalidDirection):
            scores[dirNr] = 0
            if(dirs[dirNr]==UP):
                newCoords = {"x":AIwormCoords[HEAD]["x"], "y":AIwormCoords[HEAD]["y"]-1}
            elif(dirs[dirNr]==DOWN):
                newCoords = {"x":AIwormCoords[HEAD]["x"], "y":AIwormCoords[HEAD]["y"]+1}
            elif(dirs[dirNr]==LEFT):
                newCoords = {"x":AIwormCoords[HEAD]["x"]-1, "y":AIwormCoords[HEAD]["y"]}
            elif(dirs[dirNr]==RIGHT):
                newCoords = {"x":AIwormCoords[HEAD]["x"]+1, "y":AIwormCoords[HEAD]["y"]}

            if newCoords['x'] == -1:
                newCoords['x'] = CELLWIDTH-1
            elif newCoords['x'] == CELLWIDTH:
                newCoords['x'] = 0
            elif newCoords['y'] == -1:
                newCoords['y'] = CELLHEIGHT-1
            elif newCoords['y'] == CELLHEIGHT:
                newCoords['y'] = 0
            #----------checks the distance of the apples-------------------------

            apple1dist = getClosestDist(newCoords, apple1Coords)
            apple2dist = getClosestDist(newCoords, apple2Coords)


            if(apple1dist<apple2dist):
                scores[dirNr]+=apple1dist*distScoreMultip
            else:
                scores[dirNr]+=apple2dist*distScoreMultip
            #--------makes sure there are always some open spots the snake can go (I have done this with a DFS)
            virtCoords = newCoords
            virtDir = dirs[dirNr]
            
            while(len(VisitedNodes[dirNr])<minPosMoves):
                for posDir in range(len(dirs)):
                    if(dirs[posDir]==UP and virtDir!=DOWN):
                        obsCoords = {"x":virtCoords["x"], "y":virtCoords["y"]-1, "dir":UP}
                        if(not isOcupied(obsCoords, AIwormCoords, OTwormCoords) and not ListContains(obsCoords, VisitedNodes[dirNr]) and not inWall(walls, obsCoords)):
                            ImportantNodes[dirNr].insert(0, obsCoords)
                            VisitedNodes[dirNr].insert(0, obsCoords)
                
                    elif(dirs[posDir]==DOWN and virtDir!=UP):
                        obsCoords = {"x":virtCoords["x"], "y":virtCoords["y"]+1, "dir":DOWN}
                        if(not isOcupied(obsCoords, AIwormCoords, OTwormCoords) and not ListContains(obsCoords, VisitedNodes[dirNr]) and not inWall(walls, obsCoords)):
                            VisitedNodes[dirNr].insert(0, obsCoords)
                            ImportantNodes[dirNr].insert(0, obsCoords)

                    elif(dirs[posDir]==LEFT and virtDir!=RIGHT):
                        obsCoords = {"x":virtCoords["x"]-1, "y":virtCoords["y"], "dir":LEFT}
                        if(not isOcupied(obsCoords, AIwormCoords, OTwormCoords) and not ListContains(obsCoords, VisitedNodes[dirNr]) and not inWall(walls, obsCoords)):
                            VisitedNodes[dirNr].insert(0, obsCoords)
                            ImportantNodes[dirNr].insert(0, obsCoords)

                    elif(dirs[posDir]==RIGHT and virtDir!=LEFT):
                        obsCoords = {"x":virtCoords["x"]+1, "y":virtCoords["y"], "dir":RIGHT}
                        if(not isOcupied(obsCoords, AIwormCoords, OTwormCoords) and not ListContains(obsCoords, VisitedNodes[dirNr]) and not inWall(walls, obsCoords)):
                            VisitedNodes[dirNr].insert(0, obsCoords)
                            ImportantNodes[dirNr].insert(0, obsCoords)

                if(len(ImportantNodes[dirNr])==0):
                    scores[dirNr]+=BlockinPenalty
                    break
                

                virtCoords = ImportantNodes[dirNr].pop(0)
                virtDir = virtCoords["dir"]
            
            #------------------check is thete is a posibility for the snake to touch the other snakes head-------------
            if((newCoords["x"]==OTwormCoords[HEAD]["x"]+1 and newCoords["y"]==OTwormCoords[HEAD]["y"]) or (newCoords["x"]==OTwormCoords[HEAD]["x"]-1 and newCoords["y"]==OTwormCoords[HEAD]["y"]) or (newCoords["x"]==OTwormCoords[HEAD]["x"] and newCoords["y"]==OTwormCoords[HEAD]["y"]+1) or (newCoords["x"]==OTwormCoords[HEAD]["x"] and newCoords["y"]==OTwormCoords[HEAD]["y"]-1)):
                scores[dirNr]+=inHeadPenalty

            #------makes sure there are always multiple ways the snake can go to prevent blocking in-------------
            
            for nextDirs in dirs:
                if(nextDirs==UP and dirs[dirNr]!=DOWN):
                    nextPosibleCoods = {"x":newCoords["x"], "y":newCoords["y"]-1}
                elif(nextDirs==DOWN  and dirs[dirNr]!=UP):
                    nextPosibleCoods = {"x":newCoords["x"], "y":newCoords["y"]+1}
                elif(nextDirs==LEFT and dirs[dirNr]!=RIGHT):
                    nextPosibleCoods = {"x":newCoords["x"]-1, "y":newCoords["y"]}
                elif(nextDirs==RIGHT  and dirs[dirNr]!=LEFT):
                    nextPosibleCoods = {"x":newCoords["x"]+1, "y":newCoords["y"]}
                else:
                    continue

                if nextPosibleCoods['x'] == -1:
                    nextPosibleCoods['x'] = CELLWIDTH-1
                elif nextPosibleCoods['x'] == CELLWIDTH:
                    nextPosibleCoods['x'] = 0
                elif nextPosibleCoods['y'] == -1:
                    nextPosibleCoods['y'] = CELLHEIGHT-1
                elif nextPosibleCoods['y'] == CELLHEIGHT:
                    nextPosibleCoods['y'] = 0
                
                if(not isOcupied(nextPosibleCoods, AIwormCoords, OTwormCoords) and not inWall(walls, nextPosibleCoods)):
                    escapeRoutes[dirNr]+=1
            
            if(escapeRoutes[dirNr]<minEscapeRoutes):
                scores[dirNr]+=notEnoughEscapeRoutesPenalty
                


            #----------makes sure the snake doesn't touch walls and other worms-----------------
            for coords in AIwormCoords:
                if(newCoords["x"]==coords["x"] and newCoords["y"]==coords["y"]):
                    scores[dirNr] = -1

                    

            for coords in OTwormCoords:
                if(newCoords["x"]==coords["x"] and newCoords["y"]==coords["y"]):
                    scores[dirNr] = -1

            if inWall(walls, newCoords):
                scores[dirNr] = -1
                    

        else:
            scores[dirNr]=-1 

    for scoreNr in range(len(dirs)):
        
        if(scores[scoreNr]<lowestScore and scores[scoreNr]!=-1):
            lowestScore=scores[scoreNr]
            lowestScoreNr = scoreNr
    

    #showPath(VisitedNodes[lowestScoreNr], color, minPosMoves)
    return dirs[lowestScoreNr]

    

def getClosestDist(coords1, coords2):    
    mapDis = math.sqrt((coords2["x"]-coords1["x"])**2 + (coords2["y"]-coords1["y"])**2) #gets the distance if you go through the map
    LDis = math.sqrt((coords1["x"]+WINDOWWIDTH-coords2["x"])**2 + (coords1["y"]-coords2["y"])**2)   #gets the distance if you go through the left wall
    RDis = math.sqrt((coords2["x"]+WINDOWWIDTH-coords1["x"])**2 + (coords1["y"]-coords2["y"])**2)  #gets the distance if you go through the right wall
    UDis = math.sqrt((coords1["x"]-coords2["x"])**2 + (WINDOWHEIGHT-coords1["y"]+coords2["y"])**2)   #gets the distance if you go throught the upper wall
    DDis = math.sqrt((coords1["x"]-coords2["x"])**2 + (coords1["y"]+WINDOWHEIGHT-coords2["y"])**2)   #gets the distance if you go through the downwards wall=

    distances = [mapDis, LDis, RDis, UDis, DDis]
    closestDist = 1000
    for dist in distances:
        if(dist<closestDist):   #gets the smallest distance
            closestDist=dist
    
    return closestDist  #returns smallest distance


def isOcupied(tileCoords, worm1coords, worm2coords):
    for coords in worm1coords:
        if(tileCoords['x']==coords["x"]and tileCoords['y']==coords["y"]):
            return True

    for coords in worm2coords:
        if(tileCoords['x']==coords["x"]and tileCoords['y']==coords["y"]):
            return True
    return False

def ListContains(item, list):
    for element in list:
        if(item["x"]==element["x"]and item["y"]==element["y"]):
            return True
    return False


def showPath(coordsList, color, minPosMoves):
    for coords in coordsList:
        OutherPathSquare = pygame.Rect(coords["x"]*CELLSIZE, coords["y"]*CELLSIZE, CELLSIZE, CELLSIZE) #I seperated it because I intent to make it faster by not always redrawing the entire screne every time
        pygame.draw.rect(DISPLAYSURF, color, OutherPathSquare)


    if(len(coordsList)<minPosMoves):
        print("risky path taken")
        time.sleep(1)

#---------------------------------- end of AI code -----------------------------------------------------

def drawWalls(wallList):
    for wallElement in wallList:
        for brick in wallElement:
            wallOuterBrick = pygame.Rect(brick["x"]*CELLSIZE, brick["y"]*CELLSIZE, CELLSIZE, CELLSIZE) #I sperated it because I intent to make it faster by not always redrawing the entire screne every time
            pygame.draw.rect(DISPLAYSURF, DARKGRAY, wallOuterBrick)
            wallInnerBrick = pygame.Rect(brick["x"]*CELLSIZE+5, brick["y"]*CELLSIZE+5, CELLSIZE-10, CELLSIZE-10) #I sperated it because I intent to make it faster by not always redrawing the entire screne every time
            pygame.draw.rect(DISPLAYSURF, GRAY, wallInnerBrick)


def inWall(wallList, coords):
    for wallElement in wallList:
        for brick in wallElement:
            if(brick["x"]==coords["x"]and brick["y"]==coords["y"]):
                return True
    
    return False

def placeNewApple(walls, worm1coords, worm2coords):
    apple = getRandomLocation()
    while inWall(walls, apple) or isOcupied(apple, worm1coords, worm2coords):
        apple = getRandomLocation()
    return apple
    

if __name__ == '__main__':
    main()
