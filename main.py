import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN, BLACK
from grid import Grid
import math
from constants import TOP_BOTTOM_PAD

HEIGHT = 680
WIDTH = int((3 * HEIGHT) / 2)  # 3:2 aspect ratio
BG_COLOR = DK_BLUE

# make a pygame window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BG_COLOR)

rows = 20
cols = (18 * rows) // 9  # 18:9 aspect ratio
grid = Grid(window, rows, cols)
setting_walls = False
setting_start = False
setting_goal = False
solving = False


running = True
setting_start = True
while running:
    window.fill(BG_COLOR)
    grid.draw(window)

    # Set Instructional texts and buttons
    if setting_start:
        # write "Set start node by clicking on a cell" in top left of window
        text = "Set start by clicking on the grid"
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
    elif setting_goal:
        # write "Set goal node by clicking on a cell" in top left of window
        text = "Set goal by clicking on the grid"
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
    elif setting_walls:
        # write "Set walls by clicking on cells. " in top left of window
        text = "Set walls by clicking cells. Click Solve when done."
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
        # button with text "Solve"
        pygame.draw.rect(window, LT_BLUE, (WIDTH - 100, 10, 80, 30))
        text_surface = font.render("Solve", True, DK_BLUE)
        window.blit(text_surface, (WIDTH - 90, 20))
        # if stop button is clicked, set setting_walls to False
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if WIDTH - 100 < pos[0] < WIDTH - 10 and 10 < pos[1] < 40:
                setting_walls = False
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not solving:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = math.floor((pos[1] - TOP_BOTTOM_PAD) / grid.cell_size)
                column = math.floor(
                    (pos[0] - (WIDTH - (grid.columns * grid.cell_size)) / 2) / grid.cell_size)

                if row in range(grid.rows) and column in range(grid.columns):
                    if setting_start:
                        grid.grid[row][column].set_as_start()  # set the cell as a start node
                        setting_start = False  # stop setting start node
                        setting_goal = True  # start setting goal node

                    elif setting_goal:
                        if not grid.grid[row][column].is_start:  # if the cell is not the start node
                            grid.grid[row][column].set_as_goal()  # set the cell as a goal node
                            setting_goal = False  # stop setting goal node
                            setting_walls = True  # start setting walls
                        else:  # if the cell is the start node
                            print("You can't set a goal on the start cell")
    
                    elif setting_walls:
                        if (not grid.grid[row][column].is_start) and (not grid.grid[row][column].is_goal):  # if the cell is not the start node or the goal node
                            if grid.grid[row][column].is_wall:  # if the cell is already a wall
                                grid.grid[row][column].set_as_normal()  # set the cell as a normal node
                            else:  # if the cell is not a wall
                                grid.grid[row][column].set_as_wall()  # set the cell as a wall

                    print(f"Clicked on cell ({row}, {column})")

        else:  # if solving
            pass



    pygame.display.update()
