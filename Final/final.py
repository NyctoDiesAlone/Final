# # # # DELETE ALL COMMENTS # # # #
# Constants
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import os
import time
import random
import math

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

text_font_credit = pygame.font.SysFont("Times New Roman", 15)
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
REIMU_PLAYER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Reimu_Backsprite.png')), (40, 80))
ATTACK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Test_Asset.png')), (120, 60))
HITBOX = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Hitbox.png')), (15, 15))

player_rect = HITBOX.get_rect()

FAIRY1_rect = FAIRY1.get_rect()

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

lives_current = 0 # Start with 3 lives, 0 is a game over
lives_display = str(lives_current)

bombs_current = 1 # Start with 2 bombs
bombs_display = bombs_current


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

time_event = []

bullets1 = []
bullets2 = []
bullets3 = []
bullets4 = []
frame_count = 0
def get_time(wait):
    global time_event

    if len(time_event) < wait:
        time_event.append(None)

    if len(time_event) == wait:
        time_event = []
        return True 
        
    else:
        return False
respawn_time = get_time(3)

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
        self.speed = speed * (10 ^ -3)

        self.rect = self.img.get_rect()
        

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        WIN.blit(self.img, self.rect)

    def get_center_pos(self):
        return ((self.x - (self.img.get_width() / 2) + 33), (self.y + (self.img.get_height() / 2)) )

    def move_up(self):
        if self.y >= 0:
            self.y -= self.speed

    def move_down(self):
        if self.y <= ( HEIGHT - self.img.get_height() ):
            self.y += self.speed

    def move_left(self):
        if self.x >= 0:
            self.x -= self.speed

    def move_right(self):
        if self.x <= ( (WIDTH / 1.5) - self.img.get_width() ) :
            self.x += self.speed

class Reimu(Entity):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed)

        self.rect = HITBOX.get_rect()

    def draw(self):
        super().draw()
        self.rect.topleft = self.get_center_pos()

        if keys[pygame.K_LSHIFT]: # Draws Hitbox
            WIN.blit(HITBOX, self.rect)
        if keys[pygame.K_z]: # Draws Attack
            WIN.blit(ATTACK, (self.x - (self.img.get_width() / 2) - 20, self.y - (self.img.get_height() / 2) ))

class Enemy(Entity):
    def __init__(self, img, x, y, speed):
        super().__init__(img, x, y, speed)
        self.spell = 0 

        self.rect = self.img.get_rect()

    def draw(self):
        super().draw()

    def get_center_pos(self):
        return ((self.x - (self.img.get_width() / 2) + 65), (self.y + (self.img.get_height() / 2)) )

def calculate_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec

class Bullet:
    def __init__(self, x, y, direction, speed, size):
        self.x = x 
        self.y = y
        self.image = pygame.Surface((size), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.image = pygame.transform.rotate(self.image, direction)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.direction = direction
        self.speed = speed

    def update(self, WIN_rect):
        self.pos = (calculate_new_xy(self.pos, self.speed, - self.direction))
        self.rect.center = round(self.pos[0]), round(self.pos[1])
        if not WIN_rect.colliderect(self.rect):
            return True  # Indicates bullet is offscreen
        return False

class Main:
    def __init__(self):
        # Is this my eternal punishment?
        self.cursor = Cursor_Class(WIDTH - 300, int(HEIGHT / 2) + 25)

        self.player = Reimu(REIMU_PLAYER, 200, 500, 10)
        self.enemy = Enemy(FAIRY1, WIDTH / 4, 100, 10)
        
        self.current_music = None

    def music(self):
        global pause
        if mode[level] == 0 or mode[level] == 1:
            if self.current_music is not TITLE_MUSIC:
                pygame.mixer.music.load(TITLE_MUSIC)
                pygame.mixer.music.play(-1, 0.0, 1500)
                self.current_music = TITLE_MUSIC
            pygame.mixer.music.unpause()

        elif mode[level] == 3:
            if self.current_music is not STAGE_1:
                pygame.mixer.music.load(STAGE_1)
                pygame.mixer.music.play(-1, 0.0, 1500)
                self.current_music = STAGE_1
            pygame.mixer.music.unpause()
            if pause:
                pygame.mixer.music.pause()

    def menu_control(self):
        global keys
        global mode
        global level
        global menu_bool
        global pause
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

        if pause:
            menu_bool = True

            if keys[pygame.K_UP] and self.cursor.y > (HEIGHT / 2) - 80:
                self.cursor.y -= 90
            if keys[pygame.K_DOWN] and self.cursor.y < (HEIGHT / 2) + 10:
                self.cursor.y += 90
            if keys[pygame.K_RETURN]:
                if self.cursor.y == (HEIGHT / 2) - 80:
                    menu_bool = False
                    pause = False
                if self.cursor.y == (HEIGHT / 2) + 10:
                    level = 0
                    pause = False
                    self.cursor.x = WIDTH - 300
                    self.cursor.y = int(HEIGHT / 2) + 25
                    clock.tick(delay_slow)

            self.cursor.draw()

    


    def draw_screen(self):
        global keys
        global mode
        global level
        global menu_bool
        global pause
        global used_continue
        global respawn
        global bullets
        global frame_count
        global bombs_current
        global lives_current
        control_txt_1 = Text_Draw(280, HEIGHT - 40)
        control_txt_2 = Text_Draw(280, HEIGHT - 20)

        def draw_ui():
            WIN.blit(INFO_PANEL, (WIDTH - (WIDTH / 3), 0))
            UI_LIVES.draw_large("Lives: ", (0, 0, 0))
            life_text.draw_large(lives_display, (0, 255, 0))

            UI_BOMBS.draw_large("Bombs: [X]", (0, 0, 0))
            bomb_text.draw_large(str(bombs_display), (0, 255, 0))

        def gameplay():
            global keys
            global mode
            global level
            global menu_bool
            global pause

            global used_continue
            global respawn

            global bullets1
            global bullets2
            global bullets3
            global bullets4
            global frame_count

            global bombs_current
            global lives_current

            def owch():
                global lives_current
                global menu_bool
                global keys

                global used_continue
                global respawn
                global respawn_time
                if bullet.rect.colliderect(self.player) and not respawn:
                    self.player.x = 200 
                    self.player.y = 500
                    lives_current -= 1
                    respawn_time = False
                    respawn = True

                if respawn:
                    if respawn_time:
                        respawn = False


            if not pause and not menu_bool:
                # Despawns Bullets
                for bullet in bullets1[:]:  
                    if bullet.update(WIN.get_rect()):
                        bullets1.remove(bullet)
                for bullet in bullets2[:]:  
                    if bullet.update(WIN.get_rect()):
                        bullets2.remove(bullet)
                for bullet in bullets3[:]:  
                    if bullet.update(WIN.get_rect()):
                        bullets3.remove(bullet)
                for bullet in bullets4[:]:  
                    if bullet.update(WIN.get_rect()):
                        bullets4.remove(bullet)

                if self.enemy.spell == 0:
                    if (frame_count % 10) == 0:
                        bullets1.append(Bullet(self.enemy.get_center_pos()[0], self.enemy.get_center_pos()[1], frame_count, 10, (10, 10)))
                    if (frame_count % 20) == 0:
                        bullets2.append(Bullet(self.enemy.get_center_pos()[0], self.enemy.get_center_pos()[1], -frame_count, 5, (15, 15)))
                    if (frame_count % 5) == 0:
                        bullets3.append(Bullet(self.enemy.get_center_pos()[0], self.enemy.get_center_pos()[1], .5 * (frame_count), 10, (10, 10)))
                    if (frame_count % 5) == 0:
                        bullets4.append(Bullet(self.enemy.get_center_pos()[0], self.enemy.get_center_pos()[1], -2 * (frame_count), 10, (10, 10)))


                    frame_count += 1

                    for bullet in bullets1:
                        WIN.blit(bullet.image, bullet.rect)

                        owch()
                    for bullet in bullets2:
                        WIN.blit(bullet.image, bullet.rect)

                        owch()
                    for bullet in bullets3:
                        dif = self.enemy.y - bullet.y 

                        WIN.blit(bullet.image, bullet.rect)
                        
                        owch()
                    for bullet in bullets4:
                        WIN.blit(bullet.image, bullet.rect)
                        

                        owch()

                        

                if keys[pygame.K_UP]:
                    self.player.move_up()
                if keys[pygame.K_DOWN]:
                    self.player.move_down()
                if keys[pygame.K_LEFT]:
                    self.player.move_left()
                if keys[pygame.K_RIGHT]:
                    self.player.move_right()
                if keys[pygame.K_x]: # Bomb # Doesnt update display...
                    if bombs_current != 0 and bombs_current > 0:
                        bullets1 = []
                        bullets2 = []
                        bullets3 = []
                        bullets4 = []
                        bombs_current -= 1
                        
                        
                if keys[pygame.K_LSHIFT]: # Slow
                    self.player.speed = 5
                else:
                    self.player.speed = 10

                if keys[pygame.K_ESCAPE]: # Pause
                    self.cursor.x = (WIDTH / 2) - 140
                    self.cursor.y = (HEIGHT / 2) - 80
                    pause = True

        if not pause:
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


        if pause:
            menu_bool = True
            WIN.blit(SUSPEND, (0, 0))
            PAUSE_TXT = Text_Draw((WIDTH / 2) - 170, (HEIGHT / 2) - 150)
            control_txt_1 = Text_Draw((WIDTH / 2) - 130, HEIGHT - 40)

            PAUSE_OPTION_1 = Text_Draw((WIDTH / 2) - 100, (HEIGHT / 2) - 80)
            PAUSE_OPTION_2 = Text_Draw((WIDTH / 2) - 100, (HEIGHT / 2) + 10)

            PAUSE_TXT.draw_large("~~ P A U S E D ~~", (255, 255, 255))

            PAUSE_OPTION_1.draw_large("~ Resume ~", (255, 255, 255))
            PAUSE_OPTION_2.draw_large("~ Quit ~", (255, 255, 255))

            control_txt_1.draw_small("Press arrow keys to move cursor. Enter to select.", (255, 255, 255))

        self.cursor.draw()

        if not menu_bool:
            if not pause:
                UI_LIVES = Text_Draw(550, 30)
                life_text = Text_Draw(570, 55)
                UI_BOMBS = Text_Draw(550, 90)
                bomb_text = Text_Draw(570, 115)
                if mode[level] == 3:
                    WIN.blit(STAGE_1_BG, (0, 0))
                    self.player.draw()

                    self.enemy.draw()
                        
                gameplay()
                draw_ui()

        pygame.display.flip()


    def main(self):
        self.music()
        self.draw_screen()
        self.menu_control()

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

