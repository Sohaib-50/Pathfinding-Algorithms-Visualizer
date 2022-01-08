import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN, BLACK
from grid import Grid
import math
from constants import TOP_BOTTOM_PAD, ROWS, COLS, BG_COLOR
from algorithms import DepthFirstSearch, BreadthFirstSearch, UniformCostSearch, GreedyBestFirstSearch, AStarSearch

HEIGHT = 680  
WIDTH = int((3 * HEIGHT) / 2)  # 3:2 aspect ratio

# make a pygame window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BG_COLOR)

grid = Grid(window, ROWS, COLS)
drawing_walls = False
removing_walls = False
setting_walls = False
setting_start = False
setting_goal = False
solving = False
solved = False

running = True
setting_start = True
while running:
    pygame.time.Clock().tick(120)  # limit to 120 FPS
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
                solving = True

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
                        # set the cell as a start node
                        grid.grid[row][column].set_as_start()
                        setting_start = False  # stop setting start node
                        setting_goal = True  # start setting goal node

                    elif setting_goal:
                        # if the cell is not the start node
                        if not grid.grid[row][column].is_start:
                            # set the cell as a goal node
                            grid.grid[row][column].set_as_goal()
                            setting_goal = False  # stop setting goal node
                            setting_walls = True  # start setting walls
                        else:  # if the cell is the start node
                            print("You can't set a goal on the start cell")

                    print(f"Clicked on cell ({row}, {column})")

            if (event.type == pygame.MOUSEMOTION) and setting_walls and (drawing_walls or removing_walls):
                pos = pygame.mouse.get_pos()
                row = math.floor((pos[1] - TOP_BOTTOM_PAD) / grid.cell_size)
                column = math.floor(
                    (pos[0] - (WIDTH - (grid.columns * grid.cell_size)) / 2) / grid.cell_size)
                if row in range(grid.rows) and column in range(grid.columns):
                    # if the cell is not the start node or the goal node
                    if (not grid.grid[row][column].is_start) and (not grid.grid[row][column].is_goal):
                        if drawing_walls:
                            grid.grid[row][column].set_as_wall()
                        elif removing_walls:
                            grid.grid[row][column].set_as_normal()

            if event.type == pygame.MOUSEBUTTONUP:
                drawing_walls = False
                removing_walls = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # right click
                    removing_walls = True
                if event.button == 1:  # left click
                    drawing_walls = True

    if solving:
        algorithm = AStarSearch(window)
        result = algorithm.start_solving(grid)
        if result:
            solving = False
            setting_start = True
            setting_goal = False
            setting_walls = False
            for path_node in result:
                # print("Drawing path")
                grid.grid[path_node.row][path_node.column].set_as_path()
                grid.draw(window)
                pygame.display.update()
            import time
            time.sleep(5)
            grid.reset()
        else:
            # print("No solution found")
            solving = False
            setting_start = True
            setting_goal = False
            setting_walls = False
            grid.reset()


    pygame.display.update()


