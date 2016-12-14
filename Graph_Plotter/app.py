'''
    GRAPH PLOTTER
    

'''


import math
import pygame
from pygame import *

# bygbutton: library for creating buttons
import pygbutton

# inputbox: library for creating inputbox
import inputbox


# All the raw and evaluated equations is stored in 
# the list equations.
# format: [{'raw': 'sin(x)', 'evaluated': 'math.sin(x)'}, ...]
equations = []

# initialize pygame
pygame.init()

# initialize system fonts and custom fonts along with their sizes.
font = pygame.font.SysFont('Verdana', 16)
font2 = pygame.font.SysFont('Serif', 24)
opensans14 = pygame.font.Font("opensans/OpenSans-Regular.ttf", 14)
inconsolata14 = pygame.font.Font("Inconsolata/Inconsolata-Regular.ttf", 14)

# store commonly used colors as a tuple for quick use.
white = (255, 255, 255)
black = (0, 0, 0)
titlecolor = (100, 100, 200)
graphcolor = (200, 0, 200) #purple
gridcolor = (100, 250, 240) #light blue


# surface sizing

# width and height of the graph paper.
width, height = 600, 600

# width of the graph details
extraW = 400

##############################
#                    #       #
#                    #       #
#                    #       #
#                    #  400  #
#     600 x 600      #   x   #
#                    #  600  #
#                    #       #
#                    #       #
#                    #       #
##############################

# creates window
screen = pygame.display.set_mode((width + extraW, height))

# sets title for the window and and paints white.
pygame.display.set_caption("Graph Plotter")
screen.fill(white)


def draw_equations(k):
  '''
  Draws the equations on the graph paper.
  @param {integer} k Total pixels per grid (scaling factor).
  '''

  # tells the pygame to draw only within the graph width and height.
  screen.set_clip(0, 0, width, height)

  # loops through equations and extracts evaluated equations
  # to draw it on the graph.
  for equation in equations:
    eq = equation['evaluated']
    for i in range(width):
      # use of try except for handling exceptions such as
      # division by zero 
      try:
        x = (width / 2 - i) / float(k)
        y = eval(eq)
        pos1 = (width / 2 + x * k, height / 2 - y * k)
        nx = x = (width / 2 - (i + 1)) / float(k)
        ny = eval(eq)
        pos2 = (width / 2 + nx * k, height / 2 - ny* k)
        pygame.draw.line(screen, graphcolor, pos1, pos2, 3)
      except:
        pass

  screen.set_clip(None)



def graphpaper(k):
  '''
  Draws graph paper.
  @param {integer} k Total pixels per grid (scaling factor).
  '''

  screen.set_clip(0, 0, width, height)
  screen.fill(white)

  # draws grids 
  for i in range(width / k):
    gridx = k * i
    gridy = k * i

    # draws vertical grid
    pygame.draw.line(screen, gridcolor, (gridx, 0), (gridx, height), 1)

    # draws horizontal grid
    pygame.draw.line(screen, gridcolor, (0, gridy), (width, gridy), 1)

  # extra thick line to separate graph
  # from the side window
  pygame.draw.line(screen, (200, 200, 200), (width, 0), (width, height), 3)

  # calculates and draws thick axes
  midx, midy = width / (2 * k), height / (2 * k)
  pygame.draw.line(screen, black, (midx * k, 0), (midx * k, height), 3)
  pygame.draw.line(screen, black, (0, midy * k), (width, midy * k), 3)

  screen.set_clip(None)


def listEquations(screen):
  '''
  Lists all the equations on the screen.
  @param {Object} screen The screen where equations are to be listed.
  '''

  # initialize x and y coordinates.
  y = 100
  x = width + 10

  count = 0 # total equations listed

  # loop through equations and list the raw equations that
  # was entered by the user.
  for equation in equations:
    raw_equation = equation['raw']
    textequation = inconsolata14.render(raw_equation, 1, black)
    screen.blit(textequation, (x, y + count * 50))
    count += 1

  screen.set_clip(None)


def clearScreen(screen):
  '''
  Clears the screen.
  @param {Object} screen The screen to be cleared.
  '''
  screen.set_clip(0, 0, width + extraW, height)
  screen.fill(white)


def drawTitle(screen):
  '''
  Draws title on the screen.
  @param {Object} screen The screen where title is to be drawn.
  '''

  # draw background box for title
  pygame.draw.rect(screen, (240, 240, 240), pygame.Rect((width, 0, extraW, 50)), 0)
  pygame.draw.line(screen, (200, 200, 200), (width, 50), (width + extraW, 50))

  # create and draw title
  title = font2.render("Graph Plotter" , 1, black)
  screen.blit(title, (width + 10, 10))


def validate(raw_equation):
  '''
  Validates the raw equation given by the user.
  @param {Object} screen The screen where title is to be drawn.
  @return {Object} Evaluated equation if valid equation, otherwise False
  '''

  #x = 0.0000000001 # test value set near to zero. prevents division by zero
  evaluated_equation = False
  try:
    # replace trig functions with python understandable versions
    evaluated_equation = raw_equation.replace('sin', 'math.sin')
    evaluated_equation = evaluated_equation.replace('cos', 'math.cos')
    evaluated_equation = evaluated_equation.replace('tan', 'math.tan')
    # if error occurs during evaluation, there is possibility of
    # error in the given equation.
    eval(evaluated_equation) 
    return evaluated_equation
  except:
    return False

def push_equation(raw, evaluated):
  '''
  Pushes the new equation to the list of equations.
  @param raw The raw equation given by the user.
  @ param evaluated The evaluated equation understandable by python.
  '''
  equations.append({
    'raw': raw,
    'evaluated': evaluated
  })

def new_equation_handler():
  '''
  Ask user for equation on new input.
  '''
  
  # creates input box
  userinput = inputbox.ask(screen, "Enter your equation: y =")

  # get evaluated equation (python undersdable form)
  evaluated_equation = validate(userinput)

  # add the equation to equations list if valid.
  if evaluated_equation != False:
    push_equation(userinput, evaluated_equation)


def main():
  # pixels per grid
  # also works as the scaling factor.
  k = 25

  # active is set to True when the program is running.
  active = True

  # mouse motion is not needed. Blocking mouse move saves processor.
  pygame.event.set_blocked(MOUSEMOTION)

  # creates "New Equation" button
  btnNewEquation = pygbutton.PygButton((width + 10, 60, 200, 30), 'New Equation', (100,100,255))

  while active:
    # updating the screen
    clearScreen(screen) # clear screen
    graphpaper(k) #  draw graph paper
    draw_equations(k) # draw equations
    drawTitle(screen) # draw title

    screen.set_clip(None)

    # paints the button on to the screen
    btnNewEquation.draw(screen)

    # lists all the equations on the screen
    listEquations(screen)

    # repaints the screen
    # Update portions of the screen for software displays
    pygame.display.update()

    # wait for an event
    event = pygame.event.wait()

    if event.type == pygame.QUIT:
      # set active to False and get out of the main loop
      active = False
    if 'click' in btnNewEquation.handleEvent(event):
      # btnNewEquation click event listener
      new_equation_handler()


    # pygame.time.wait(20)
  # exits the program
  pygame.quit()

if __name__ == '__main__':
  main()
  
