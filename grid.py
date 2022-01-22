import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN, BLACK
from constants import TOP_BOTTOM_PAD
from random import shuffle

class Node:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.color = LT_GREY
        self.is_goal = False
        self.is_start = False
        self.is_wall = False
        self.parent = None
        self.is_path = False
        self.path_cost = 0
        self.state = (self.row, self.column)
        
    def set_as_start(self):
        self.is_start = True
        self.color = DK_BLUE

    def set_as_goal(self):
        self.is_goal = True
        self.color = GREEN

    def set_as_wall(self):
        self.is_wall = True
        self.color = BLACK

    def set_as_path(self):
        self.is_path = True
        self.color = LT_BLUE

    def set_as_normal(self):
        self.is_wall = False
        self.is_goal = False
        self.is_start = False
        self.is_path = False
        self.parent = None
        self.color = LT_GREY

    def set_as_visited(self):
        self.color = DK_GREY

    def __str__(self):
        return f"Node({self.row}, {self.column})"

    def __ge__(self, other: "Node") -> bool:
        return self.path_cost >= other.path_cost

    def __gt__(self, other: "Node") -> bool:
        return self.path_cost > other.path_cost

    def __le__(self, other: "Node") -> bool:
        return self.path_cost <= other.path_cost

    def __lt__(self, other: "Node") -> bool:
        return self.path_cost < other.path_cost

    def __eq__(self, other: "Node") -> bool:
        return self.path_cost == other.path_cost

    def __ne__(self, other: "Node") -> bool:
        return self.path_cost != other.path_cost

    def __hash__(self):
        return hash((self.row, self.column))



class Grid:
    def __init__(self, window, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[Node(row, column) for column in range(columns)] for row in range(rows)]
        grid_height = window.get_height() - (TOP_BOTTOM_PAD * 2)
        self.cell_size = grid_height // rows
        self.y_start = TOP_BOTTOM_PAD
        self.x_start = (window.get_width() - (self.columns * self.cell_size)) // 2

    def draw(self, window):
        for row in self.grid:
            for cell in row:
                pygame.draw.rect(window, cell.color, (self.x_start + cell.column * self.cell_size, self.y_start + cell.row * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(window, BLACK, (self.x_start + cell.column * self.cell_size, self.y_start + cell.row * self.cell_size, self.cell_size, self.cell_size), 2)

    def draw_cell(self, window, node):
        pygame.draw.rect(window, node.color, (self.x_start + node.column * self.cell_size, self.y_start + node.row * self.cell_size, self.cell_size, self.cell_size))
        pygame.draw.rect(window, BLACK, (self.x_start + node.column * self.cell_size, self.y_start + node.row * self.cell_size, self.cell_size, self.cell_size), 2)
        
    def get_start_node(self) -> Node:
        for row in self.grid:
            for cell in row:
                if cell.is_start:
                    return cell
    
    def get_goal_node(self) -> Node:
        for row in self.grid:
            for cell in row:
                if cell.is_goal:
                    return cell

    def get_neighbors(self, node):
        # NOTE: Don't allow diagonal movement or else it will pass through walls (untill a solution is found)
        neighbors = []
        left_coordinate = (node.row, node.column - 1)
        right_coordinate = (node.row, node.column + 1)
        top_coordinate = (node.row - 1, node.column)
        bottom_coordinate = (node.row + 1, node.column)
        # diagonal_top_left = (node.row - 1, node.column - 1)
        # diagonal_top_right = (node.row - 1, node.column + 1)
        # diagonal_bottom_left = (node.row + 1, node.column - 1)
        # diagonal_bottom_right = (node.row + 1, node.column + 1)

        if self.is_valid_coordinate(*left_coordinate) and not self.grid[left_coordinate[0]][left_coordinate[1]].is_wall:
            neighbors.append(self.grid[left_coordinate[0]][left_coordinate[1]])
        if self.is_valid_coordinate(*right_coordinate) and not self.grid[right_coordinate[0]][right_coordinate[1]].is_wall:
            neighbors.append(self.grid[right_coordinate[0]][right_coordinate[1]])
        if self.is_valid_coordinate(*top_coordinate) and not self.grid[top_coordinate[0]][top_coordinate[1]].is_wall:
            neighbors.append(self.grid[top_coordinate[0]][top_coordinate[1]])
        if self.is_valid_coordinate(*bottom_coordinate) and not self.grid[bottom_coordinate[0]][bottom_coordinate[1]].is_wall:
            neighbors.append(self.grid[bottom_coordinate[0]][bottom_coordinate[1]])
        # if self.is_valid_coordinate(*diagonal_top_left) and not self.grid[diagonal_top_left[0]][diagonal_top_left[1]].is_wall:
        #     neighbors.add(self.grid[diagonal_top_left[0]][diagonal_top_left[1]])
        # if self.is_valid_coordinate(*diagonal_top_right) and not self.grid[diagonal_top_right[0]][diagonal_top_right[1]].is_wall:
        #     neighbors.add(self.grid[diagonal_top_right[0]][diagonal_top_right[1]])
        # if self.is_valid_coordinate(*diagonal_bottom_left) and not self.grid[diagonal_bottom_left[0]][diagonal_bottom_left[1]].is_wall:
        #     neighbors.add(self.grid[diagonal_bottom_left[0]][diagonal_bottom_left[1]])
        # if self.is_valid_coordinate(*diagonal_bottom_right) and not self.grid[diagonal_bottom_right[0]][diagonal_bottom_right[1]].is_wall:
        #     neighbors.add(self.grid[diagonal_bottom_right[0]][diagonal_bottom_right[1]])
        shuffle(neighbors)
        return neighbors

        # if node.row > 0 and not self.grid[left_coordinate[0]][left_coordinate[1]].is_wall:
        #     neighbors.append(self.grid[left_coordinate[0]][left_coordinate[1]])
        # if node.row < self.rows - 1 and not self.grid[right_coordinate[0]][right_coordinate[1]].is_wall:
        #     neighbors.append(self.grid[right_coordinate[0]][right_coordinate[1]])
        # if node.column > 0 and not self.grid[top_coordinate[0]][top_coordinate[1]].is_wall:
        #     neighbors.append(self.grid[top_coordinate[0]][top_coordinate[1]])
        # if node.column < self.columns - 1 and not self.grid[bottom_coordinate[0]][bottom_coordinate[1]].is_wall:
        #     neighbors.append(self.grid[bottom_coordinate[0]][bottom_coordinate[1]])

        # return neighbors

    def get_manhattan_distance_heuristic(self, node1: Node,):
        goal = self.get_goal_node()
        return abs(node1.row - goal.row) + abs(node1.column - goal.column)
        # import math
        # return math.sqrt((node1.column - node2.column) ** 2 + (node1.row - node2.row) ** 2)

    def is_valid_coordinate(self, row, column):
        return row >= 0 and row < self.rows and column >= 0 and column < self.columns

    def reset(self, keep_current_configuration=False):
        for row in self.grid:
            for cell in row:
                cell.parent = None
                if not keep_current_configuration:
                    cell.set_as_normal()
                else:
                    if cell.is_start:
                        cell.set_as_start()
                    elif cell.is_goal:
                        cell.set_as_goal()
                    elif cell.is_wall:
                        cell.set_as_wall()
                    else:
                        cell.set_as_normal()
                # if keep_current_configuration:
                #     if not any([cell.is_start, cell.is_goal, cell.is_wall]):  # if cell isn't start, goal or wall
                #         cell.set_as_normal()
                # else:
                #     cell.set_as_normal()
                
