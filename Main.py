import pygame
import sys
from pygame.locals import *

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

infoObject = pygame.display.Info()
gameDispaly = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
icon = pygame.image.load("aud/icon.png")       
pygame.display.set_icon(icon)

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0,0 )
light_red= (255, 0, 0)
green = (0, 170, 0)
light_green = (0, 255, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
glow = (0, 125, 255)

#image pos and sizes
title_posX = int(infoObject.current_w/3.5)
title_posY = int(infoObject.current_h/13)
title_width = int(infoObject.current_w/2.5)
title_height = int(infoObject.current_h/6.5)
cred_button_width = int(title_width/4.5)
char_button_width = int(title_width/3)
char_but_pos = int(title_width/25)
char_button_height = int(title_width/10) 
char_but_posY = int(infoObject.current_h/3) 
quit_butX = int(infoObject.current_w/1.15)

#music
pygame.mixer.music.load("aud/menumusic1.WAV")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)


#images
background = pygame.image.load("aud/sky.jpg")
new_game_button = pygame.image.load("aud/new.png")
leaderboard_button = pygame.image.load("aud/board.png")
back_button = pygame.image.load("aud/plane.jpg")
header = pygame.image.load("aud/title.png")
quit_but = pygame.image.load("aud/exit.png")


#size convertions
background = pygame.transform.scale(background, (infoObject.current_w, infoObject.current_h))
header = pygame.transform.scale(header, (title_width, title_height))
new_game_button = pygame.transform.scale(new_game_button, (cred_button_width, char_button_height))
leaderboard_button = pygame.transform.scale(leaderboard_button, (cred_button_width, char_button_height))                
quit_but = pygame.transform.scale(quit_but, (cred_button_width, char_button_height))

                                  
clock = pygame.time.Clock()


def image_blit():
    gameDispaly.blit(header, (title_posX, title_posY))                                
    gameDispaly.blit(new_game_button, (title_posX + char_but_pos, char_but_posY))                                
    gameDispaly.blit(leaderboard_button, (title_posX + char_but_pos + char_button_width, char_but_posY))
    gameDispaly.blit(quit_but, (quit_butX, char_but_posY))




def introLoop():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()

            gameDispaly.blit(background,(0,0))
            image_blit()

            button(title_posX, char_but_posY, char_button_width, char_button_height, glow, action = "ng")
            button(title_posX + char_button_width, char_but_posY, char_button_width, char_button_height, glow, action = "lead")
            button(quit_butX, char_but_posY, cred_button_width, char_button_height, glow, action = "quit")

            pygame.display.update()
            clock.tick(60)

def button(x, y, width, height, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width>cur[0]>x and y + height>cur[1]>y:
      pygame.draw.rect(gameDispaly, active_color, (x,y, width, height))
      image_blit()
      if click[0] == 1 and action != None:
            print("")
            if action == "quit":
                pygame.quit()
                quit()

                 
            elif action == "ng":
                 print("New Game")
                 
            elif action == "lead":
                 print("Leaderboard")


introLoop()
                
               
    





                                  
       
