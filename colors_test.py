import pygame
from colors import LT_BLUE, LT_GREY, DK_GREY, RED, DK_BLUE, GREEN 

HEIGHT = 680
WIDTH = int((3 * HEIGHT) / 2)
background_color = (0, 0, 0)

# make a pygame window
pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(background_color)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(background_color)
    pygame.draw.rect(window, LT_GREY, pygame.Rect(0, 30, WIDTH, 30))
    pygame.draw.rect(window, DK_GREY, pygame.Rect(0, 60, WIDTH, 30), 30)
    pygame.draw.rect(window, GREEN, pygame.Rect(0, 102, WIDTH, 30), 30)
    pygame.draw.rect(window, DK_BLUE, pygame.Rect(0, 120, WIDTH, 30), 30)
    pygame.draw.rect(window, LT_BLUE, pygame.Rect(0, 170, WIDTH, 30), 30)
    pygame.draw.rect(window, RED, pygame.Rect(0, 210, WIDTH, 30), 30)
    pygame.display.update()


