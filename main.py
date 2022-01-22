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

# state variables
drawing_walls = False
removing_walls = False
setting_walls = False
setting_start = False
setting_goal = False
choosing_algo = False
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
                choosing_algo = True
    elif choosing_algo:
        # write "Choose an algorithm by clicking on a button" in top left of window
        text = "Choose an algorithm by clicking on a button"
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
        # draw buttons for each algorithm horizontally across the top of the window
        pygame.draw.rect(window, LT_BLUE, (10, 10, 80, 30))
        text_surface = font.render("Depth-First", True, DK_BLUE)
        window.blit(text_surface, (20, 20))
        pygame.draw.rect(window, LT_BLUE, (100, 10, 80, 30))
        text_surface = font.render("Breadth-First", True, DK_BLUE)
        window.blit(text_surface, (110, 20))
        pygame.draw.rect(window, LT_BLUE, (190, 10, 80, 30))
        text_surface = font.render("Uniform-Cost", True, DK_BLUE)
        window.blit(text_surface, (200, 20))
        pygame.draw.rect(window, LT_BLUE, (280, 10, 80, 30))
        text_surface = font.render("Greedy-Best", True, DK_BLUE)
        window.blit(text_surface, (290, 20))
        pygame.draw.rect(window, LT_BLUE, (370, 10, 80, 30))
        text_surface = font.render("A*", True, DK_BLUE)
        window.blit(text_surface, (380, 20))
        # logic for button clicking / choosing algorithms
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if 10 < pos[0] < 90 and 10 < pos[1] < 40:
                algorithm = DepthFirstSearch(window)
                choosing_algo = False
                solving = True
            elif 100 < pos[0] < 180 and 10 < pos[1] < 40:
                algorithm = BreadthFirstSearch(window)
                choosing_algo = False
                solving = True
            elif 190 < pos[0] < 270 and 10 < pos[1] < 40:
                algorithm = UniformCostSearch(window)
                choosing_algo = False
                solving = True
            elif 280 < pos[0] < 360 and 10 < pos[1] < 40:
                algorithm = GreedyBestFirstSearch(window)
                choosing_algo = False
                solving = True
            elif 370 < pos[0] < 450 and 10 < pos[1] < 40:
                algorithm = AStarSearch(window)
                choosing_algo = False
                solving = True
    elif solving:
        window.fill(BG_COLOR)
        # write "Solving..." in top left of window
        text = "Solving..."
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
        grid.draw(window)
        # algorithm = GreedyBestFirstSearch(window)
        result = algorithm.start_solving(grid)
        if result:
            for path_node in result:
                # print("Drawing path")
                grid.grid[path_node.row][path_node.column].set_as_path()
                grid.draw(window)
                pygame.display.update()
        solving = False
        solved = True
        # write "Solved!" in top left of window
        text = "Solved!" if result else "No Possible solution"
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, LT_BLUE)
        window.blit(text_surface, (10, 10))
    elif solved:
        # button with text "Choose algorithm again
        pygame.draw.rect(window, LT_BLUE, (WIDTH - 100, 10, 80, 30))
        text_surface = font.render("Choose algorithm again", True, DK_BLUE)
        window.blit(text_surface, (WIDTH - 90, 20))
        # button with text "Reset"
        pygame.draw.rect(window, LT_BLUE, (WIDTH - 200, 10, 80, 30))
        text_surface = font.render("Reset", True, DK_BLUE)
        window.blit(text_surface, (WIDTH - 190, 20))
        # buttons clicking logic
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if WIDTH - 100 < pos[0] < WIDTH - 10 and 10 < pos[1] < 40:
                print("Choose algorithm again")
                grid.reset(keep_current_configuration=True)
                choosing_algo = True
                solved = False
            elif WIDTH - 200 < pos[0] < WIDTH - 10 and 10 < pos[1] < 40:
                print("Reset")
                grid.reset()
                solved = False
                setting_start = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if setting_start or setting_goal or setting_walls:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = math.floor((pos[1] - TOP_BOTTOM_PAD) / grid.cell_size)
                column = math.floor((pos[0] - (WIDTH - (grid.columns * grid.cell_size)) / 2) / grid.cell_size)

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
        pass


    pygame.display.update()


