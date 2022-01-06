import frontiers
import pygame

class DepthFirstSearch:
    def __init__(self, window):
        self.window = window
        self.frontier = frontiers.QueueFrontier()
        # self.frontier = frontiers.StackFrontier()

    def start_solving(self, grid):
        visited = set()
        

        running = True
        while not self.frontier.empty() and running:
            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_node = self.frontier.remove()  
            if current_node.is_goal:  # goal test
                return self.build_path(current_node)

            current_node.set_as_visited()  
            visited.add(current_node)
            neighbors = grid.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = current_node
                    self.frontier.add(neighbor)
            grid.draw_cell(self.window, current_node)  # draw current node to show it is visited
            pygame.display.update()
            
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
            