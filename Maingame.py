import pygame, sys

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)

background_colour = (0,0,0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AoS')


plane = pygame.image.load("aud/plane.jpg")
plane_top = screen.get_height() - plane.get_height()
plane_left = screen.get_width()/2 - plane.get_width()/2



screen.blit(plane, (plane_left,plane_top))

shot = pygame.image.load("aud/bullet.png")
shoot_y = 0

while True:
    clock.tick(60)
    screen.fill((0,0,0))
    x,y = pygame.mouse.get_pos()
    screen.blit(plane, (x-plane.get_width()/2, plane_top))
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
    
