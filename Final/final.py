# # # # DELETE ALL COMMENTS # # # #
# Constants
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import os
import time
import pymunk

pygame.init()
pygame.mixer.init()
pygame.font.init()
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

text_font_credit = pygame.font.SysFont("Ariel", 15)
text_font_description = pygame.font.Font("Rage.ttf", 40)
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
TITLE_QUIT = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Title_Quit.png')), (300, 150)) # "Quit" button on Title Screen


SHOT_DEFENSE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Shot_A.png')), (400, 200)) # Shot A
SHOT_OFFENSE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Shot_B.png')), (400, 200)) # Shot B

# Gameplay
INFO_PANEL = pygame.image.load(os.path.join('Assets', 'Info_Panel.png'))
# RESOURCE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Resource.png')), (25, 25))

FAIRY1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Fairy1.png')), (70, 70)) # Dark
FAIRY2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Fairy2.png')), (70, 70)) # Light

PLACEHOLDER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Test_Asset.png')), (40, 80))
ATTACK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Test_Asset.png')), (120, 60))
HITBOX = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Hitbox.png')), (15, 15))

player_rect = PLACEHOLDER.get_rect()
player_mask = pygame.mask.from_surface(PLACEHOLDER)

FAIRY1_rect = FAIRY1.get_rect()
bullet_mask = pygame.mask.from_surface(FAIRY1)

# Level Backgrounds
STAGE_1_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'STAGE_1.png')), (WIDTH / 1.5, HEIGHT))

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

# Gameplay 
pause = False
used_continue = False
respawn = False
shot_type_a = True 

lives_total = [0, 1, 2, 3, 4, 5, 6] # 6 max lives is reasonable
lives_current = 3 # Start with 3 lives, 0 is a game over
lives_display = str(lives_current)

bombs_total = [0, 1, 2, 3, 4, 5, 6] # 6 max bombs
bombs_current = 2 # Start with 2 bombs
bombs_display = str(bombs_current)


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
STAGE_1 = "Shrine at the Foot of the Mountain.mp3"
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

class Text_Draw:
	def __init__(self, x, y):
		self.x = x 
		self.y = y  
	def draw_small(self, text, text_color):
		img_text = text_font_credit.render(text, True, text_color)
		WIN.blit(img_text, (self.x, self.y))
	def draw_large(self, text, text_color):
		img_text = text_font_description.render(text, True, text_color)
		WIN.blit(img_text, (self.x, self.y))

class Entity:
	def __init__(self, img, x, y, speed, health=0):
		self.img = img
		self.x = x 
		self.y = y 
		self.health = health
		self.speed = speed
	def draw(self):
		WIN.blit(self.img, (self.x, self.y))	
	def get_center_pos(self):
		return ((self.x - (self.img.get_width() / 2) - 20), (self.y - (self.img.get_height() / 2)) )

class Reimu(Entity):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed) 


    def draw(self):
        super().draw()
        if keys[pygame.K_LSHIFT]: # Draws Hitbox
        	WIN.blit(HITBOX, (self.x + (int(self.img.get_width()) / 2) - 6, (self. y + (int(self.img.get_height()) / 2) - 2) ) )
        if keys[pygame.K_z]: # Draws Attack
        	WIN.blit(ATTACK, (self.x - (self.img.get_width() / 2) - 20, self.y - (self.img.get_height() / 2) ))
    def collision(self):
    	self.damn_hitbox = pygame.mask.from_surface(HITBOX)
    	return self.damn_hitbox
    def collision_pos(self):
    	self.player_rect = HITBOX.get_rect()
    	return self.player_rect



class Enemy(Entity):
    def __init__(self, img, x, y, speed, health, type_):
        super().__init__(img, x, y, speed, health)
        self.type_ = type_

    
    def draw(self):
        super().draw()

    def collision(self):
    	self.torment = pygame.mask.from_surface(self.img)
    	return self.torment
    def collision_pos(self):
    	self.bullet_rect = self.img.get_rect()
    	return self.bullet_rect



class Main:
    def __init__(self):
        # Is this my eternal punishment?
        self.cursor = Cursor_Class(WIDTH - 300, int(HEIGHT / 2) + 25)

        self.player = Reimu(PLACEHOLDER, 200, 500, 10)
        self.player_hitbox = self.player.collision()
        self.player_hitbox_pos = self.player.collision_pos()

        self.bullet = Enemy(PLACEHOLDER, 0, 0, 0, 10, 0)
        self.bullet_hitbox = self.bullet.collision()
        self.bullet_hitbox_pos = self.bullet.collision_pos()

        self.current_music = None

    

    # This is why we cant have nice things
    def music(self):
        if mode[level] == 0 or mode[level] == 1:
            if self.current_music is not TITLE_MUSIC:
                pygame.mixer.music.load(TITLE_MUSIC)
                pygame.mixer.music.play(-1, 0.0, 1500)
                self.current_music = TITLE_MUSIC
            
        elif mode[level] == 3 and not pause:
            if self.current_music is not STAGE_1:
                pygame.mixer.music.load(STAGE_1)
                pygame.mixer.music.play(-1, 0.0, 1500)    
                self.current_music = STAGE_1  
	    	  
    def menu_control(self):
        global keys
        global mode
        global level
        global menu_bool
        global run # Needed for "Quit" button to work"


        if level == 0 or level == 1 or level == 2:
            menu_bool = True
        else:
            menu_bool = False

        if menu_bool:
        	if keys[pygame.K_ESCAPE]:
	        	if mode[level] != 0:
	        		level = 0
	        		# default cursor pos
	        		self.cursor.x = WIDTH - 300
	        		self.cursor.y = int(HEIGHT / 2) + 25
	        		clock.tick(delay_slow) # Some buttons should register slower to avoid annoyance.
	        
        	if mode[level] == 0:
	        	if keys[pygame.K_UP] and self.cursor.y > int(HEIGHT / 2) + 25:
	        		self.cursor.y -= 65
	        		time.sleep(.2)
	        	if keys[pygame.K_DOWN] and self.cursor.y < (int(HEIGHT / 2) + 200):
	        		self.cursor.y += 65
	        		time.sleep(.2)
	        	if keys[pygame.K_RETURN]:
	        		if self.cursor.y == (int(HEIGHT / 2) + 25): # Cursor over "Play"
	        			level = 1
	        			self.cursor.x = WIDTH - 430
	        			self.cursor.y = 50
	        			time.sleep(.5)
	        			
	        		if self.cursor.y == (int(HEIGHT / 2) + 155): # Cursor over "Credits"
	        			level = 2
	        			time.sleep(.5)

	        		if self.cursor.y == (int(HEIGHT / 2) + 220): # Cursor over "Quit""
	        			run = False

	        if mode[level] == 1:
		        if keys[pygame.K_UP] and self.cursor.y > 50:
		        	self.cursor.y -= 150
		        	time.sleep(.2)
		        if keys[pygame.K_DOWN] and self.cursor.y < 200:
		        	self.cursor.y += 150
		        	time.sleep(.2)
		        	
		        if keys[pygame.K_SPACE]:
		        	if self.cursor.y == 50:
		        		level = 3

    def gameplay(self):
    	global keys
    	global mode
    	global level
    	global menu_bool
    	global pause
    	global used_continue
    	global respawn

    	if not pause and not menu_bool:
    		if self.player_hitbox.overlap(self.bullet_hitbox, (self.player_hitbox_pos[0] - self.bullet_hitbox_pos[0], self.player_hitbox_pos[1] - self.bullet_hitbox_pos[1])):
    			print("mad")
    		
    		if keys[pygame.K_UP] and self.player.y >= 0:
    			self.player.y -= self.player.speed
    		if keys[pygame.K_DOWN] and self.player.y <= (HEIGHT - self.player.img.get_height() ):
    			self.player.y += self.player.speed
    		if keys[pygame.K_LEFT] and self.player.x >= 0:
    			self.player.x -= self.player.speed
    		if keys[pygame.K_RIGHT] and self.player.x <= ( (WIDTH / 1.5) - self.player.img.get_width() ) :
    			self.player.x += self.player.speed
    		if keys[pygame.K_x]: # Bomb
    			pass 
    		if keys[pygame.K_z]: # Attack
    			pass

    		if keys[pygame.K_LSHIFT]: # Slow
    			self.player.speed = 5
    		else:
    			self.player.speed = 10
    		if keys[pygame.K_ESCAPE]: # Pause
    			pause = True
    	if pause:
    		menu_bool = True
    		if keys[pygame.K_UP]: 
    			pass
    		if keys[pygame.K_DOWN]:
    			pass
    		if keys[pygame.K_RETURN]:
    			pass
					
					
    def draw_screen(self):
        global menu_bool
        global pause
        control_txt_1 = Text_Draw(280, HEIGHT - 40)
        control_txt_2 = Text_Draw(280, HEIGHT - 20)

        def draw_ui():
        	WIN.blit(INFO_PANEL, (WIDTH - (WIDTH / 3), 0))
        	UI_LIVES.draw_large("Lives: ", (0, 0, 0))
        	life_text.draw_large(lives_display, (0, 255, 0))
        	
        	UI_BOMBS.draw_large("Bombs: [X]", (0, 0, 0))
        	bomb_text.draw_large(bombs_display, (0, 255, 0))


        if mode[level] == 0: # Main Menu
        	# Background Assets
            WIN.blit(TITLE_BG, (0, 0))
            WIN.blit(TITLE_LOGO, (-50, -30))
            # Aesthetics

            # Buttons
            WIN.blit(TITLE_PLAY, (WIDTH - 250, int(HEIGHT / 2)))
            WIN.blit(TITLE_PRACTICE, (WIDTH - 250, int(HEIGHT / 2) + 80))
            WIN.blit(TITLE_CREDITS, (WIDTH - 250, int(HEIGHT / 2) + 140))
            WIN.blit(TITLE_QUIT, (WIDTH - 250, int(HEIGHT / 2) + 190))

            control_txt_1.draw_small("Press arrow keys to move cursor. Enter to select.", (0, 0, 0))
            
            # Misc
            self.cursor.draw()

        if mode[level] == 1: # Shot Selection Menu
        	
        	# TXT Objects for Defense
        	DES1 = Text_Draw(115, HEIGHT / 2)
        	DES2 = Text_Draw(350, HEIGHT / 2)

        	DES3 = Text_Draw(70, (HEIGHT / 2) + 40)
        	DES4 = Text_Draw(220, (HEIGHT / 2) + 40)
        	DES5 = Text_Draw(420, (HEIGHT / 2) + 40)
        	DES6 = Text_Draw(120, (HEIGHT / 2) + 80)

        	DES7 = Text_Draw(70, (HEIGHT / 2) + 150)
        	DES8 = Text_Draw(120, (HEIGHT / 2) + 190)
        	# Extra TXT Objects
        	DES1a = Text_Draw(30, HEIGHT / 2)
        	DES3a = Text_Draw(10, (HEIGHT / 2) + 40)
        	DES4a = Text_Draw(160, (HEIGHT / 2) + 40)
        	


        	WIN.blit(TITLE_BG, (0, 0))
        	WIN.blit(TITLE_LOGO, (-50, -30))
        	WIN.blit(SUSPEND, (0, 0))

        	WIN.blit(SHOT_DEFENSE, (WIDTH /2, 20))
        	WIN.blit(SHOT_OFFENSE, (WIDTH /2, 170))
        	self.cursor.draw()

        	if self.cursor.y == 50:
        		DES1.draw_large("Death Bombing", (255, 0, 0))
        		DES2.draw_large("does not consume a bomb!", (0, 0, 0))
        		DES3.draw_large("   Captured", (0, 0, 0))
        		DES4.draw_large("  Spell Cards", (255, 0, 0))
        		DES5.draw_large("drop life fragments,", (0, 0, 0))
        		DES6.draw_large("collect 4  for an extra life.", (0, 0, 0))
        		DES7.draw_large("Ideal for those who enjoy some lienience", (0, 0, 0))
        		DES8.draw_large("on their journy...", (0, 0, 0))

        	if self.cursor.y == 200:
        		DES1a.draw_large("Time your attacks to increase its velocity and damage!", (0, 0, 0))
        		DES3a.draw_large(" Capturing", (0, 0, 0))
        		DES4a.draw_large(" Spell Cards", (255, 0, 0))
        		DES4.draw_large("             temporarily spawns another orb.", (0, 0, 0))
        		DES7.draw_large("Nothing stands in your path unscathed!", (0, 0, 0))
        		DES8.draw_large("Just dont scathe yourself in the process.", (0, 0, 0))

        	control_txt_1.draw_small("Press arrow keys to move cursor. Space to select.", (0, 0, 0))
        	control_txt_2.draw_small("            Press Escape to go back.", (0, 0, 0))


        if mode[level] == 2: # Legal
        	WIN.blit(TITLE_BG, (0, 0))

        	# TXT objects
        	ZUN_1 = Text_Draw(50, 20)
        	ZUN_2 = Text_Draw(100, 40)
        	PICHUUN_CREDIT = Text_Draw(100, 60)

        	MENU_SELECT_SFX_CREDIT = Text_Draw(50, 100)
        	PIXABAY_WEBSITE = Text_Draw((WIDTH / 2) + 70, 100)
        	MS_SFX_URL = Text_Draw(100,120)

        	ZUN_1.draw_small("Touhou is ZUNs property, not mine. I aint that weird!", (0, 0, 0))
        	ZUN_2.draw_small("# All characters and music are property under ZUN", (0, 0, 0))
        	PICHUUN_CREDIT.draw_small("# Sound effect which plays upon Reimu losing a life (known as a Pichuun) is property of ZUN", (0, 0, 0))

        	MENU_SELECT_SFX_CREDIT.draw_small("Menu confirmation sfx (A-Selection-Menus.mp3) from Pixabay.com", (0, 0, 0))
        	PIXABAY_WEBSITE.draw_small("https://pixabay.com", (255, 0, 0))
        	MS_SFX_URL.draw_small("https://pixabay.com/sound-effects/select-denied-04-96602/", (0, 0, 0))

        	control_txt_1.draw_small("            Press Escape to go back.", (0, 0, 0))

        if not menu_bool: 

        	UI_LIVES = Text_Draw(550, 30)
        	life_text = Text_Draw(570, 55)
        	UI_BOMBS = Text_Draw(550, 90)
        	bomb_text = Text_Draw(570, 115)
        	if not pause:
        		if mode[level] == 3:
        			WIN.blit(STAGE_1_BG, (0, 0))

        			self.player.draw()
        			self.bullet.draw()

        			draw_ui()


        pygame.display.flip()

    def main(self):
        self.music()
        self.menu_control()
        self.draw_screen()
        self.gameplay()

main_object = Main()

def test(): # FXN for bugfixing. Ignore.
    print(runtime())
    print(level)
    print(" ")
	
while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    test() # Bugfixing. Delete

    main_object.main()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

