# Constants
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import os
import time
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Touhou")

""" Window and Gameplay """
WIDTH = 800
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

run = True
CURSOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Cursor.png')), (30, 30))
# Menus
	# Title Screen
TITLE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_BG.png')), (WIDTH, HEIGHT))
TITLE_LOGO = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Logo.png')), (600, 400))
TITLE_PLAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Play.png')), (200, 100))
TITLE_CREDITS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Credits.png')), (200, 100))

"""Menu and Level handlers"""
		# 0 = main Menu
		# 1 = character select
		# 2 = stage 1 
		# # -1 = credits + ending
mode = [0, 1,  2, 3]
level = 0
menu_bool = False

"""CONTROLS"""

delay = 5

"""Music"""
TITLE_MUSIC = pygame.mixer.music.load("Sealed Gods.mp3")
"""SFX"""
# DEATH = pygame.mixer.music.load("Pichuun.mp3")

# What?
class Cursor_Class:
	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.img = CURSOR 
	def draw(self):
		WIN.blit(self.img, (self.x, self.y))
	def get_pos(self):
		return (self.x, self.y)

def main():
	cursor = Cursor_Class(0, 0)
	def music():
		if not pygame.mixer.music.get_busy():
			if mode[level] == 0 or mode[level] == 1:
				pygame.mixer.music.play(-1, 0.0, 1500)

	def menu_control():
		global keys
		global mode 
		global level
		global menu_bool
		if level == 0 or level == 1:
			menu_bool = True
		else:
			menu_bool = False
		if menu_bool:
			WIN.blit(cursor, (0, 0))

			if keys[pygame.K_UP]:
				print("up")
			if keys[pygame.K_DOWN]:
				print("down")
			if keys[pygame.K_RETURN]:
				print("select")

	def draw_screen():
		global menu_bool

		if mode[level] == 0: # main menu
			WIN.blit(TITLE_BG, (0, 0))
			WIN.blit(TITLE_LOGO, (-50, -30))
			
			WIN.blit(TITLE_PLAY, (WIDTH - 200, HEIGHT / 2))
			WIN.blit(TITLE_CREDITS, (WIDTH - 200, (HEIGHT / 2) + 70))

		pygame.display.flip()


	music()
	menu_control()
	draw_screen()
while run:
	clock.tick(FPS)
	keys = pygame.key.get_pressed()
	
	main()
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False

