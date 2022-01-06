import frontiers
import pygame

class DepthFirstSearch:
    def __init__(self, window):
        self.window = window
        self.frontier = frontiers.QueueFrontier()
        # self.frontier = frontiers.StackFrontier()

    def start_solving(self, grid):
        visited = set()
        start = grid.get_start()
        self.frontier.add(start)
        running = True
        print("Start node: ", start)
        while not self.frontier.empty() and running:
            # pygame.time.Clock().tick(0.5)  # 60 FPS
            print(f"Visited: {len(visited)}, Frontier: {len(self.frontier)}")

            # check for exit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current = self.frontier.remove()  
            print(f"Current node: {current}")
            # print(current.row, current.column)
            if current.is_goal:
                return self.build_path(current)

            current.set_as_visited() if not current.is_start else None
            visited.add(current)
            print(f"visited: {[(node.row, node.column) for node in visited]}")
            neighbors = grid.get_neighbors(current)
            # print(f"Neighbors: {[(n.row, n.column) for n in neighbors]}")
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor.parent = current
                    self.frontier.add(neighbor)
            grid.draw_cell(self.window, current)
            pygame.display.update()
            print(f"Frontier: {self.frontier}")
            # print([node for node in self.frontier.self.frontier])
        # print("FAILURE")
        if not running:
            pygame.display.quit()
            pygame.quit()
        return None
            
    def build_path(self, node):
        path = []
        while node.parent is not None:
            print("building path")
            path.append(node)
            node = node.parent
        path.reverse()
        print("Built path")
        print(self.frontier)
        return path
            