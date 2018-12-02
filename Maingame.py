import pygame, sys

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(1)

background_colour = (0,0,0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AoS')


plane = pygame.image.load("aud/plane.png")
plane_top = screen.get_height() - plane.get_height()
plane_left = screen.get_width()/2 - plane.get_width()/2

screen.blit(plane, (plane_left,plane_top))


while True:
    clock.tick(60)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

