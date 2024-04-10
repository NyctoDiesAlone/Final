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
CURSOR = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Cursor.png')), (30, 30)) # Cursor Icon used for various menus
# Menus
DISPLAY_PIC = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Cursor.png')), (32, 32)) # Small Window Img 
pygame.display.set_icon(DISPLAY_PIC)
"""
Drawn on top of background assets
# Semi-transparent darkening filter for menu backgrounds:
	# Pause
	# Shot Select
"""
SUSPEND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Suspend.png')), (WIDTH, HEIGHT))

# Title Screen
TITLE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_BG.png')), (WIDTH, HEIGHT)) # Background for "mode" 0, 1, 2
TITLE_LOGO = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Logo.png')), (600, 400)) # Touhou: Trail of the Shrine Maiden
TITLE_PLAY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Play.png')), (200, 100)) # "Play" button on Title Screen
TITLE_PRACTICE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Prac.png')), (200, 100)) # "Practice Start" button on Title Screen
TITLE_CREDITS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Credits.png')), (200, 100)) # "Credits" button on Title Screen

TEST_A = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'test_button_a.png')), (200, 100))
TEST_B = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'test_button_b.png')), (200, 100))
"""Menu and Level handlers"""
        # 0 = main Menu
        # 1 = character select
        # 2 = practice start menu
        # # -1 = credits + ending
mode = [0, 1,  2, 3]
level = 0
# Dictates whether a menu is open 
# Includes Title Screen + similar
menu_bool = False 

"""CONTROLS"""
""" RUNTIME BY FRAMES FOR TESTING """
temp_runtime = 0
def runtime():
    global temp_runtime
    while  temp_runtime > -1:
        temp_runtime += 1
        return temp_runtime

delay = 10 # Button delay for menus. trying to select stuff when cursor is moving at 60FPS is a pain.
delay_slow = int(delay / 3) # Some buttons should register slower to avoid annoyance.

"""Music"""
TITLE_MUSIC = "Sealed Gods.mp3"
"""SFX"""
DEATH = "Pichuun.mp3"
MENU_SELECT_SFX = "A_Selection_Menus.mp3" # SFX for menu selection (pressing RETURN)

# Universal Cursor Param 
# For Menus
class Cursor_Class:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = CURSOR
    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
    def get_pos(self):
        return (self.x, self.y)

def screen_change():
    delta = 0
    if delta == level:
        return True
    else:
        return False

class Main:
    # Make a flag which detects a change in mode[level]. Could fix the cursor not changing between screens. 
    # This is why we can't have nice things. 

    def __init__(self):
        # Is this my eternal punishment?
        if screen_change():
            if mode[level] == 0:
                self.cursor = Cursor_Class(WIDTH - 300, int(HEIGHT / 2) + 25)
                
            if mode[level] == 1:
                self.cursor = Cursor_Class(0, 0)
    

    """
    Doesnt play SFX, so overlapping sounds and switching tracks might be a problem.
    Creating a class could work?
    """
    def music(self):
        if not pygame.mixer.music.get_busy(): # Python audio playing is dumb
            if mode[level] == 0 or mode[level] == 1:
                pygame.mixer.music.load(TITLE_MUSIC)
                pygame.mixer.music.play(-1, 0.0, 1500)
                """
                # Doesnt work. 
                if keys[pygame.K_RETURN] and menu_bool: # Selection ping for menuing
                    pygame.mixer.music.load(MENU_SELECT_SFX)
                    pygame.mixer.music.play(0, 0.0, 0)
                """
			



    def menu_control(self):
        global keys
        global mode
        global level
        global menu_bool
        if level == 0 or level == 1:
            menu_bool = True
        else:
            menu_bool = False

        if menu_bool:
        	if keys[pygame.K_ESCAPE]:
        		if mode[level] != 0:
        			level = 0
        			clock.tick(delay_slow) # Some buttons should register slower to avoid annoyance.
        	if keys[pygame.K_UP] and self.cursor.y > int(HEIGHT / 2) + 25:
        		self.cursor.y -= 65
        		clock.tick(delay)
        	if keys[pygame.K_DOWN] and self.cursor.y < (int(HEIGHT / 2) + 140):
        		self.cursor.y += 65
        		clock.tick(delay)
        	if keys[pygame.K_RETURN]:
        		if (mode[level] == 0): # Title Screen 
        			if self.cursor.y == (int(HEIGHT / 2) + 25): # Cursor over "Play"
        				level = 1
        				clock.tick(delay_slow)

    def draw_screen(self):
        global menu_bool

        if mode[level] == 0: # Main Menu
        	# Background Assets
            WIN.blit(TITLE_BG, (0, 0))
            WIN.blit(TITLE_LOGO, (-50, -30))
            # Aesthetics

            # Buttons
            WIN.blit(TITLE_PLAY, (WIDTH - 250, int(HEIGHT / 2)))
            WIN.blit(TITLE_PRACTICE, (WIDTH - 250, int(HEIGHT / 2) + 80))
            WIN.blit(TITLE_CREDITS, (WIDTH - 250, int(HEIGHT / 2) + 140))
            
            # Misc
            self.cursor.draw()

        if mode[level] == 1: # Shot Selection Menu
            
            WIN.blit(TITLE_BG, (0, 0))
            WIN.blit(SUSPEND, (0, 0))

        	# Misc
            self.cursor.draw()


        

        pygame.display.flip()

    def main(self):
        self.music()
        self.menu_control()
        self.draw_screen()

main_object = Main()

def test(): # FXN for bugfixing. Ignore.
    print(runtime())
    print(level)
    print(screen_change())
    print(" ")
	
while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    test() # Bugfixing. Delete

    main_object.main()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

