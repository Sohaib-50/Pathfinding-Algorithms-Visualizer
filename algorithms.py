import frontiers
import pygame

class SearchAlgorithm:
    def __init__(self, window):
        self.window = window

    def start_solving(self, grid):
        visited = set()
        start_node = grid.get_start_node()
        self.frontier.add(start_node)
        visited.add(start_node)
        running = True
        while not self.frontier.empty() and running:
            pygame.time.Clock().tick(60)  # limit to 60 FPS
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_node = self.frontier.remove()
            current_node.set_as_visited() if (not current_node.is_start and not current_node.is_goal) else None
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
            # print(f"frontier: {self.frontier}")
            
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None

    def build_path(self, node):
        # TODO: Check why try/except is needed
        path = []
        # node = node.parent  # skip the last node
        try:
            while node.parent is not None:
                # print("building path")
                path.append(node)
                node = node.parent
        except:
            pass
            # print(f"frontier: {self.frontier}")
        path.append(node)  # add the start node which was not added in the loop
        path.reverse()
        return path  # skip the last node


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.QueueFrontier()


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.StackFrontier()

class UniformCostSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.PriorityQueueFrontier()

    def start_solving(self, grid):
        closed = set()
        self.frontier.add(grid.get_start_node())
        running = True
        while not self.frontier.empty() and running:
            pygame.time.Clock().tick(60)  # limit to 60 FPS
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            path_cost, current_node = self.frontier.remove()
            current_node.set_as_visited() if not (current_node.is_start or current_node.is_goal) else None
            if current_node.is_goal:  # goal test
                return self.build_path(current_node)
            elif current_node in closed:
                continue
            else:
                # expand current node
                closed.add(current_node)
                neighbors = grid.get_neighbors(current_node)
                for neighbor in neighbors:
                    if neighbor not in closed:
                        neighbor.parent = current_node
                        self.frontier.add(neighbor, current_node.path_cost)
                        
            grid.draw_cell(self.window, current_node)  # draw current node to show it is visited
            pygame.display.update()
            # print(f"frontier: {self.frontier}")
                
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None


class AStarSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.AStarPriorityQueueFrontier()

    def start_solving(self, grid):
        closed = set()
        self.frontier.add(grid.get_start_node(), -1, grid)
        running = True
        # print(self.frontier)
        while not self.frontier.empty() and running:
            pygame.time.Clock().tick(60)  # limit to 60 FPS
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            cost, current_node = self.frontier.remove()
            current_node.set_as_visited() if not (current_node.is_start or current_node.is_goal) else None
            if current_node.is_goal:  # goal test
                return self.build_path(current_node)
            elif current_node in closed:
                continue
            else:
                # expand current node
                # TODO: Seperate out functionalities of this function like expansion to reduce code duplication
                closed.add(current_node)
                neighbors = grid.get_neighbors(current_node)
                for neighbor in neighbors:
                    if neighbor not in closed:
                        neighbor.parent = current_node
                        self.frontier.add(neighbor, current_node.path_cost, grid)
                        
            grid.draw_cell(self.window, current_node)  # draw current node to show it is visited
            pygame.display.update()
            # print(f"frontier: {self.frontier}")
                
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None
    
class GreedyBestFirstSearch(SearchAlgorithm):
    def __init__(self, window):
        super().__init__(window)
        self.frontier = frontiers.GreedyBestFirstPriorityQueueFrontier()

    # def start_solving(self, grid):
        # visited = set()
        # start_node = grid.get_start_node()
        # self.frontier.add(start_node)
        # visited.add(start_node)
        # running = True
        # print(self.frontier)
        # while not self.frontier.empty() and running:
        #     pygame.time.Clock().tick(60)  # limit to 60 FPS
        #     # check for exit event
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False

        #     cost, current_node = self.frontier.remove()
        #     current_node.set_as_visited() if not (current_node.is_start or current_node.is_goal) else None
        #     if current_node.is_goal:  # goal test
        #         return self.build_path(current_node)
        #     elif current_node in closed:
        #         continue
        #     else:
        #         # expand current node

    def start_solving(self, grid):
        visited = set()
        start_node = grid.get_start_node()
        self.frontier.add(start_node, grid)
        visited.add(start_node)
        running = True
        while not self.frontier.empty() and running:
            pygame.time.Clock().tick(60)  # limit to 60 FPS
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            heuristic, current_node = self.frontier.remove()
            current_node.set_as_visited() if (not current_node.is_start and not current_node.is_goal) else None
            if current_node.is_goal:  # goal test
                return self.build_path(current_node)
            # expand current node
            neighbors = grid.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = current_node
                    self.frontier.add(neighbor, grid)
                    visited.add(neighbor)
            grid.draw_cell(self.window, current_node)  # draw current node to show it is visited
            pygame.display.update()
            # print(f"frontier: {self.frontier}")
            
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None
                