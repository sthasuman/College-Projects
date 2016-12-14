# inputbox based on Timothy Down's app map editor

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    pygame.time.wait(1)
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return (event.key, event.unicode)
    else:
      pass

def display_box(screen, message, text):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font("Inconsolata/Inconsolata-Regular.ttf", 14)
  screen.set_clip(None)
  pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() / 2 - 200, screen.get_height() / 2 - 100, 400, 200), 0)
  pygame.draw.rect(screen, (50, 50, 50), (screen.get_width() / 2 - 200, screen.get_height() / 2 - 100, 400, 200), 1)
  pygame.draw.rect(screen, (200, 200, 200), (screen.get_width() / 2 - 200 + 16, screen.get_height() / 2 - 12, 400 - 32, 24), 1)

  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0)), ((screen.get_width() / 2) - 200 + 16, (screen.get_height() / 2) - 32))
    screen.blit(fontobject.render(text[-30:] + "_", 1, (0,0,0)), ((screen.get_width() / 2) - 200 + 24, (screen.get_height() / 2) - 10))
    screen.blit(fontobject.render("Press ENTER when done", 1, (190,190,190)), ((screen.get_width() / 2) - 200 + 16, (screen.get_height() / 2) + 16))

  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()

  screen.set_clip(None)
  rect = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA, 32)
  rect.fill((255, 255, 255, 200))
  screen.blit(rect, (0, 0))
  pygame.draw.rect(screen, (150, 150, 150), (screen.get_width() / 2 - 200 + 8, screen.get_height() / 2 - 100 + 8, 400, 200), 0)
  current_string = []
  display_box(screen, question, string.join(current_string,""))

  while 1:
    pygame.time.wait(1)
    inkey, unichr = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    else:
      current_string += unichr
    display_box(screen, question, string.join(current_string,""))
  return string.join(current_string,"")

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name") + " was entered"

if __name__ == '__main__': main()
