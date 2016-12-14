#!/usr/bin/env python
# -*- coding: utf-8 -*-
# zModule example6

from zModule import *
import os

def nothing():
        print "1"
        pass

def s1():
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	while True:
		clock.tick(20)

		events = pygame.event.get()
		for e in events:
			if e.type == QUIT:
				pygame.quit()
				sys.exit()
			elif e.type == KEYDOWN and e.key == K_ESCAPE:
				return

		txtbutton.update(events)
		imgbutton.update(events)
		txtimgbutton.update(events)
		screen.fill(0xffffff)
		txtbutton.draw(screen)
		imgbutton.draw(screen)
		txtimgbutton.draw(screen)
		pygame.display.flip()

#Buttons paths
b1 = os.path.join("data","b1.png")
b2 = os.path.join("data","b2.png")

if __name__ == '__main__':
	# Call zEngine inizializer
	game = zEngine()
	game.MainMenu.submenu("Buttons",s1)
	#game.MainMenu.submenu("Exit",sys.exit)
	#game.MainMenu.submenu("Exit", pygame.quit())

	#Create a zTextButton
	txtbutton = zTextButton(nothing, (50,100), "LMAO", 30, None, RED, BLUE)
	#zTextButton constructor
	#function, pos, text, dim, font=None, color=BLACK, prcolor=BLACK

	#Create a zImgButton
	imgbutton = zImgButton(nothing, (200,100), b1, b2, None)
	#zImgButton constructor
	#function, pos, image_path, primage_path=None, colorkey=None

	#Create a zTextImgButton
	txtimgbutton = zTextImgButton(nothing, (200,200), b1, "TEST", 30, None, RED, BLUE, b2, None)
	#zTextImgButton constructor
	#function, pos, image_path, text, dim, font=None, color=BLACK, prcolor=BLACK, primage_path=None, colorkey=None

	game.mainloop()

	#Try it, and you'll notice three different buttons:
	#The first is only text;
	#The second is an image;
	#The third is the first centered on the second.

