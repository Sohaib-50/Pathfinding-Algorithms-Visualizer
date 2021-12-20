import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN
from grid import Grid

HEIGHT = 680
WIDTH = int((3 * HEIGHT) / 2)  # 3:2 aspect ratio
BG_COLOR = DK_BLUE

# make a pygame window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BG_COLOR)

rows = 20
grid = Grid(window, rows, (18 * rows) // 9)

running = True
while running:
    window.fill(BG_COLOR)
    grid.draw(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()


