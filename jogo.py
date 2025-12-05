import pygame
from pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Hello Pygame")
bgcolor = (30, 30, 100)
screen.fill(bgcolor)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()