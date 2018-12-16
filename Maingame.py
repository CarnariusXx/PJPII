import pygame, sys

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)

background_colour = (0,0,0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AoS')
icon = pygame.image.load("aud/icon.png")       
pygame.display.set_icon(icon)


plane = pygame.image.load("aud/plane01.png")
plane_top = screen.get_height() - plane.get_height()
plane_left = screen.get_width()/2 - plane.get_width()/2

enemy = pygame.image.load("aud/enemy_01.png")
enemy_top = screen.get_height()/2
enemy_left = screen.get_width()/2 


screen.blit(plane, (plane_left,plane_top))
screen.blit(enemy, (enemy_left,enemy_top))

shot = pygame.image.load("aud/bullet.png")
shoot_y = 0

while True:
    clock.tick(60)
    screen.fill((0,0,0))
    x,y = pygame.mouse.get_pos()
    screen.blit(plane, (x-plane.get_width()/2, plane_top))
    screen.blit(enemy, (enemy_left,enemy_top))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot_y = 500
            shoot_x = x-45

    if shoot_y > 0:
        screen.blit(shot, (shoot_x, shoot_y))
        shoot_y -= 10
    pygame.display.update()
    
