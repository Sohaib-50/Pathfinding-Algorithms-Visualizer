import pygame
from colors import LT_BLUE, DK_BLUE, LT_GREY, DK_GREY, RED, GREEN, BLACK
from constants import TOP_BOTTOM_PAD

class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.color = LT_GREY
        self.is_goal = False
        self.is_start = False
        self.is_wall = False
        
    def set_as_start(self):
        self.is_start = True
        self.color = DK_BLUE

    def set_as_goal(self):
        self.is_goal = True
        self.color = GREEN

    def set_as_wall(self):
        self.is_wall = True
        self.color = LT_GREY

class Grid:
    def __init__(self, window, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[Cell(row, column) for column in range(columns)] for row in range(rows)]
        grid_size = window.get_height() - (TOP_BOTTOM_PAD * 2)
        self.cell_size = grid_size // rows

    def draw(self, window):
        y_start = TOP_BOTTOM_PAD
        x_start = (window.get_width() - (self.columns * self.cell_size)) // 2
        for row in self.grid:
            for cell in row:
                pygame.draw.rect(window, cell.color, (x_start + cell.column * self.cell_size, y_start + cell.row * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(window, BLACK, (x_start + cell.column * self.cell_size, y_start + cell.row * self.cell_size, self.cell_size, self.cell_size), 2)


        