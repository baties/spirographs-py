# spiro.py

# Description: drawing spirographs using math equations with python
# Tutorial from: Spirographs by Playground: Geeky Projects for the Curious
# Programmer

import turtle
import math
import numpy as np
from math import gcd
import sys
import random
import argparse
from PIL import Image
from datetime import datetime
import logging # Batis

# Class for drawing a Spirograph
class Spiro:
    # the constructor
    def __init__(self, xc, yc, col, R, r, L):
        logging.info('Spiro Class Init') # Batis

        # crate the turtle object
        self.t = turtle.Turtle()

        # self.t.setfillopacity(50)  # Batis

        # set the cursor shape
        self.t.shape('circle')  # Batis   'turtle'

        # set the drawings steps/increments in degrees
        self.step = 20  # Batis 5 

        # set the drawing complete flag
        # see https://docs.python.org/3.3/library/turtle.html
        self.drawingComplete = False

        # set the paramaters from the functions below
        self.setparams(xc, yc, col, R, r, L)

        self.t.speed(20)  # Batis

        self.lColor = False  # Batis

        # initialize the drawing
        self.restart()

    # set the parameters
    def setparams(self, xc, yc, col, R, r, L):
        logging.info('Spiro setParams') # Batis

        # the Spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.L = L

        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal

        # get ratio of radii
        self.k = r/float(R)

        # set color
        self.t.color(*col)

        # store the current angle
        self.a = 0

    # set restart method for the drawing
    def restart(self):
        logging.info('Spiro restart') # Batis

        # set the flag
        self.drawingComplete = False

        # show the turtle
        self.t.showturtle()

        # go to the first point to begin plot
        self.t.up()
        R, k, L = self.R, self.k, self.L
        a = 0.0
        x = R*((1-k)*math.cos(a) + L*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - L*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # Specify the draw method
    def draw(self):
        logging.info('Spiro draw') # Batis

        # draw the remaining points
        R, k, L, = self.R, self.k, self.L
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + L*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - L*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        # drawing is done so hide the turtle cursor
        self.t.hideturtle()

    # update the drawing by one step crating animatin effect
    def update(self):
        # logging.info('Spiro update') # Batis

        # skip remaining steps if complete
        if self.drawingComplete:
            return

        # increment the angle
        self.a += self.step

        # draw a step
        R, k, L = self.R, self.k, self.L

        # set angle
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + L*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - L*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)

        # Add by Batis
        if self.lColor == True:
            if (self.a % 360) == 0:
                sCol = (random.random(), random.random(), random.random()) # Batis  
                self.t.color(*sCol) # Batis  
        # Batis

        # if drawing is complete, set the flag
        if self.a >= 360*self.nRot:
            self.drawingComplete = True

            # drawing is done, so hide turtle cursor
            self.t.hideturtle()

    # clear everything
    def clear(self):
        logging.info('Spiro clear') # Batis
        self.t.clear()

    # Add by Batis From Here
    def toggleColor(self):
        sCol = (random.random(), random.random(), random.random()) # Batis  
        self.t.color(*sCol) # Batis  
    # Add by Batis Till Here

    # Add by Batis 
    def togglelColor(self):
        if self.lColor == False:
            self.lColor = True
        else:
            self.lColor = False
    # Batis

# class for animating the spirographs
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        logging.info('SpiroAnimator Init') # Batis

        # set the timer value in millisecords
        self.deltaT = 10

        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        print(str(self.width) + "  " + str(self.height)) # Batis

        self.Numb = 0  # Batis
        self.RrLc = [[0] * 4 for i in range(N)]  # Batis

        # crate spiro objects
        self.spiros = []
        for i in range(N):

            self.Numb  = i # Batis

            # generate random parameters
            rparams = self.genRandomParams()

            # set the spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)

        print(self.RrLc) # Batis

        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # restart the spiro drawing
    def restart(self):
        logging.info('SpiroAnimator restart') # Batis

        for spiro in self.spiros:

            # clear
            spiro.clear()

            # generate random parameters
            rparams = self.genRandomParams()

            # set the spiro parameters
            spiro.setparams(*rparams)

            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParams(self):
        logging.info('SpiroAnimator genrandomParams') # Batis

        width, height = self.width, self.height
        # R = random.randint(50, min(width, height)//2)  # Batis
        # r = random.randint(10, 9*R//10)  # Batis

        ### Added By Batis From Here
        if self.Numb == 0 :
            minR = 50
            minr = 10
        else :
            if (self.RrLc[self.Numb-1][0] < (min(width, height)//2)) :
                minR = self.RrLc[self.Numb-1][0]
            else:
                minR = 50
            if (self.RrLc[self.Numb-1][1] < (9*minR//10)):
                minr = self.RrLc[self.Numb-1][1]
            else:
                minr = 10
        ### Added By Batis till Here

        R = random.randint(minR, min(width, height)//2)  # Batis
        r = random.randint(minr, 9*R//10)  # Batis

        L = random.uniform(0.1, 0.9)
        # xc = random.randint(-width//2, width//2)  # Batis
        # yc = random.randint(-height//2, height//2)  # Batis
        xc = 0 # Batis
        yc = 0 # Batis
        col = (random.random(),
               random.random(),
               random.random()
               )

        self.RrLc[self.Numb] = [R,r,L,col]  # Batis

        print("R = " + str(R) + "  *  r = " + str(r) + "  *  L = " + str(L)) # Batis
        print(col) # Batis
        print("xc = " + str(xc) + "  *  yc = " + str(yc)) # Batis

        return(xc, yc, col, R, r, L)

    # update method
    def update(self):
        # logging.info('SpiroAnimator update') # Batis

        # Update all spiros
        numComplete = 0
        for spiro in self.spiros:

            # update
            spiro.update()

            # sCol = (random.random(), random.random(), random.random()) # Batis  (Add & Comment)
            # spiro.t.color(*sCol) # Batis  (Add & Comment)

            # count completed spiros
            if spiro.drawingComplete:
                numComplete += 1

        # restart if all spiros are complete
        # if numComplete == len(self.spiros):  # Batis
            # self.restart()  # Batis

        # call the timer
        turtle.ontimer(self.update, self.deltaT)

    # toggle cursor
    def toggleTurtles(self):
        logging.info('SpiroAnimator toggle Turtle') # Batis

        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                # if spiro.drawingComplete == True:  # Batis
                spiro.t.showturtle()

    # Add by Batis From Here
    def toggleSColor(self):
        for spiro in self.spiros:
            sCol = (random.random(), random.random(), random.random()) # Batis  
            spiro.t.color(*sCol) # Batis  
    # Add by Batis Till Here

    # Add by Batis 
    def toggleSlColor(self):
        for spiro in self.spiros:
            if spiro.lColor == False:
                spiro.lColor = True
            else:
                spiro.lColor = False
    # Batis


# save drawings to PNG files
def saveDrawing():
    logging.info('Save Drawing') # Batis

    # hide the turtle cursor
    turtle.hideturtle()

    # generate unique filenames
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    logging.info('saving drawing to %s.esp/png' % fileName)

    # get the tkinter canvas
    canvas = turtle.getcanvas()

    # save the drawings as a post script image
    canvas.postscript(file=fileName + '.eps')

    # use the Pillow module to convert the postscript image file to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')

    # show the turtle cursor
    turtle.showturtle()


# Add by Batis From Here
def toggleBKColor():
    global BKColor # Batis

    if BKColor == 'White' :
        turtle.getscreen().bgcolor('black') 
        BKColor = 'Black'
    else :
        turtle.getscreen().bgcolor('white')
        BKColor = 'White'
# Add by Batis Till Here



# The main() function
def main():
    logging.basicConfig(filename='myLog.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p') # Batis


    # use sys.argv if needed
    logging.info('generating spirograph...')

    # create parser
    descStr = """This program draws Spirographs using the turtle module.
    When run with no arguments, this program draws random Spirographs.

    Terminology:

    R: radius of outer circle
    r: radius of inner circle
    L: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparms: R, r, L")

    # parse args
    args = parser.parse_args()

    global BKColor # Batis
    BKColor = 'White'  # Batis

    global cOpacity # Batis
    cOpacity = 0.5 # 50% Color Opacity   # Batis

    # turtle.getscreen().bgcolor('black') # Batis    

    # set width of the spiro drawing window 60% of the screen width, height
    turtle.setup(width=1.0, height=1.0) # Batis width=0.6, height=0.6

    # set shape of the turtle cursor
    turtle.shape('turtle')

    # set the title to the Spirographs!
    turtle.title("Spirographs")

    # add the key handler to save your drawings
    turtle.onkey(saveDrawing, "s")

    turtle.onkey(toggleBKColor, "b") # Batis

    # start listening
    turtle.listen()

    # hide the main turtle cursor
    turtle.hideturtle()

    # check for any arguments sent to --sparams and draw the Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        print(params) # Batis

        # draw the Spirograph with the given parameters
        # col = (0.0, 0.0, 0.0)
        col = (random.random(),
               random.random(),
               random.random()
               )
        print(col) # Batis
        spiro = Spiro(0, 0, col, *params)

        turtle.onkey(spiro.toggleColor, "c") # Batis

        turtle.onkey(spiro.togglelColor, "h") # Batis

        spiro.draw()

    else:
        # create the animator object
        spiroAnim = SpiroAnimator(3) # Batis 4

        # add a keyhandler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")

        # add a keyhandler to restart the animation
        turtle.onkey(spiroAnim.restart, "space")

        turtle.onkey(spiroAnim.toggleSColor, "x") # Batis

        turtle.onkey(spiroAnim.toggleSlColor, "z") # Batis


    # start the turtle main loop
    turtle.mainloop()  


# call main
if __name__ == '__main__':
    main()
