import frontiers
import pygame

class SearchAlgorithm:
    def __init__(self, window):
        self.window = window

    def start_solving(self, grid):
        visited = set()
        self.frontier.reset()
        start_node = grid.get_start_node()
        self.frontier.add(start_node)
        running = True
        while not self.frontier.empty() and running:
            pygame.time.Clock().tick(30)
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_node = self.frontier.remove()
            current_node.set_as_visited() if not current_node.is_start else None
            visited.add(current_node)
            if current_node.is_goal:  # goal test
                return self.build_path(current_node)
            # expand current node
            neighbors = grid.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = current_node
                    self.frontier.add(neighbor)
                    visited.add(neighbor)
            grid.draw_cell(self.window, current_node)  # draw current node to show it is visited
            pygame.display.update()
            print(f"frontier: {self.frontier}")
            
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None


    def build_path(self, node):
        path = []
        try:
            while node.parent is not None:
                print("building path")
                path.append(node)
                node = node.parent
        except:
            print(f"frontier: {self.frontier}")
        path.reverse()
        print("Built path")
        print(self.frontier)
        return path


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.QueueFrontier()


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.StackFrontier()

            