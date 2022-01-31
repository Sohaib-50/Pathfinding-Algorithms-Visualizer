import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN, BLACK, WHITE
from grid import Grid
import math
from constants import TOP_BOTTOM_PAD, ROWS, COLS, BG_COLOR
from algorithms import DepthFirstSearch, BreadthFirstSearch, UniformCostSearch, GreedyBestFirstSearch, AStarSearch

HEIGHT = 680  
WIDTH = int((3 * HEIGHT) / 2)  # 3:2 aspect ratio

# make a pygame window
pygame.init()
pygame.display.set_caption('Path Finding Algorithms Visualizer')
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BG_COLOR)

grid = Grid(window, ROWS, COLS)
instructional_font = pygame.font.SysFont("roboto", 30)
button_font = pygame.font.SysFont("roboto", 25)
instructional_font_color = WHITE
button_font_color = BLACK
button_color = WHITE
button_border_color = LT_BLUE

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
    # pygame.time.Clock().tick()  # limit to 120 FPS
    window.fill(BG_COLOR)
    grid.draw(window)
    # Set Instructional texts and buttons
    if setting_start:
        text = "Set start node by clicking on the grid"
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
    elif setting_goal:
        # write "Set goal node by clicking on a cell" in top left of window
        text = "Set goal by clicking on the grid"
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
    elif setting_walls:
        # text "Set walls by clicking on cells. " in top left of window
        text = "Set walls by clicking and dragging. Press left mouse button to set, right to remove."
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
        # button with text "Choose Algorithm" below grid
        text = "Choose Algorithm"
        text_surface = button_font.render(text, True, button_font_color)
        button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        button_rect.height += 20
        button_rect.width += 20
        button_rect.center = (WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2)
        pygame.draw.rect(window, button_color, button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2)))
        # button click logic
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(pos):
                setting_walls = False
                choosing_algo = True
    elif choosing_algo:
        # text "Choose an algorithm by clicking on a button"
        text = "Select an algorithm."
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
        # buttons for each algorithm below grid
        text = "Depth First Search"
        text_surface = button_font.render(text, True, button_font_color)
        dfs_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        dfs_button_rect.height += 10
        dfs_button_rect.width += 30
        dfs_button_rect.x = 10 + 50
        dfs_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2
        pygame.draw.rect(window, button_color, dfs_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, dfs_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=dfs_button_rect.x + 5, y=dfs_button_rect.y + 5))
        text = "Breadth First Search"
        text_surface = button_font.render(text, True, button_font_color)
        bfs_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        bfs_button_rect.height += 10
        bfs_button_rect.width += 10
        bfs_button_rect.x = 200 + 50
        bfs_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2
        pygame.draw.rect(window, button_color, bfs_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, bfs_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=bfs_button_rect.x + 5, y=bfs_button_rect.y + 5))
        text = "Greedy Best First Search"
        text_surface = button_font.render(text, True, button_font_color)
        grbfs_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        grbfs_button_rect.height += 10
        grbfs_button_rect.width += 10
        grbfs_button_rect.x = 385 + 50
        grbfs_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2
        pygame.draw.rect(window, button_color, grbfs_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, grbfs_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=grbfs_button_rect.x + 5, y=grbfs_button_rect.y + 5))
        text = "Uniform Cost Search"
        text_surface = button_font.render(text, True, button_font_color)
        ucs_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        ucs_button_rect.height += 10
        ucs_button_rect.width += 10
        ucs_button_rect.x = 605 + 50
        ucs_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2
        pygame.draw.rect(window, button_color, ucs_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, ucs_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=ucs_button_rect.x + 5, y=ucs_button_rect.y + 5))
        text = "A-star Search"
        text_surface = button_font.render(text, True, button_font_color)
        astar_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        astar_button_rect.height += 10
        astar_button_rect.width += 10
        astar_button_rect.x = 790 + 50
        astar_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2
        pygame.draw.rect(window, button_color, astar_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, astar_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=astar_button_rect.x + 5, y=astar_button_rect.y + 5))
        # button click logic
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if dfs_button_rect.collidepoint(pos):
                algorithm = DepthFirstSearch(window)
                choosing_algo = False
                solving = True
            elif bfs_button_rect.collidepoint(pos):
                algorithm = BreadthFirstSearch(window)
                choosing_algo = False
                solving = True
            elif grbfs_button_rect.collidepoint(pos):
                algorithm = GreedyBestFirstSearch(window)
                choosing_algo = False
                solving = True
            elif ucs_button_rect.collidepoint(pos):
                algorithm = UniformCostSearch(window)
                choosing_algo = False
                solving = True
            elif astar_button_rect.collidepoint(pos):
                algorithm = AStarSearch(window)
                choosing_algo = False
                solving = True
    elif solving:
        window.fill(BG_COLOR)
        text = "Solving..."
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
        grid.draw(window)
        pygame.display.update()

        result = algorithm.start_solving(grid)
        if result:  # if path found
            # draw path
            for path_node in result:
                if not any((path_node.is_start, path_node.is_goal)):
                    grid.grid[path_node.row][path_node.column].set_as_path()
                    grid.draw(window)
                    pygame.display.update()
        solving = False
        solved = True
    elif solved:
        # write "Solved!" in top left of window
        if result:
            text = "Solved!"
        else:
            text = "No possible path"
        text_surface = instructional_font.render(text, True, instructional_font_color)
        window.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, TOP_BOTTOM_PAD // 2)))
        # buttons for choose algorithm again or reset below grid
        text = "Choose another algorithm"
        text_surface = button_font.render(text, True, button_font_color)
        choose_algo_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        choose_algo_button_rect.height += 20
        choose_algo_button_rect.width += 10
        choose_algo_button_rect.x = 325
        choose_algo_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2 - 20
        pygame.draw.rect(window, button_color, choose_algo_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, choose_algo_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=choose_algo_button_rect.x + 5, y=choose_algo_button_rect.y + 10))
        text = "Reset"
        text_surface = button_font.render(text, True, button_font_color)
        reset_button_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - TOP_BOTTOM_PAD // 2))
        reset_button_rect.height += 20
        reset_button_rect.width += 10
        reset_button_rect.x = 600
        reset_button_rect.y = HEIGHT - TOP_BOTTOM_PAD // 2 - 20
        pygame.draw.rect(window, button_color, reset_button_rect, border_radius=3)
        pygame.draw.rect(window, button_border_color, reset_button_rect, 2, border_radius=3)
        window.blit(text_surface, text_surface.get_rect(x=reset_button_rect.x + 5, y=reset_button_rect.y + 10))
        # buttons click logic
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if choose_algo_button_rect.collidepoint(pos):
                solved = False
                choosing_algo = True
                grid.reset(keep_current_configuration=True)
                window.fill(BG_COLOR)
                grid.draw(window)
            elif reset_button_rect.collidepoint(pos):
                solved = False
                setting_start = True
                grid.reset()
                window.fill(BG_COLOR)
                grid.draw(window)
        pygame.display.update()


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


