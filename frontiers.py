import heapq

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def reset(self):
        self.frontier = []

    def __str__(self) -> str:
        coordinates = [(node.row, node.column) for node in self.frontier]
        return str(coordinates)

    def __len__(self) -> int:
        return len(self.frontier)


class StackFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop()

    
class QueueFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop(0)


class PriorityQueueFrontier(StackFrontier):
    def add(self, node, parent_path_cost=0):
        if not self.contains_state(node.state):  # if node is not already in frontier
            node.path_cost = parent_path_cost + 1
            heapq.heappush(self.frontier, (parent_path_cost + 1, node))
        else:
            # discard node in frontier if path cost is higher than the current node
            for idx, (path_cost, frontier_node) in enumerate(self.frontier):
                if frontier_node.state == node.state:
                    if (parent_path_cost + 1) < path_cost:
                        self.frontier = self.frontier[:idx] + self.frontier[idx + 1:]
                        node.path_cost = parent_path_cost + 1
                        heapq.heappush(self.frontier, (parent_path_cost + 1, node))
                        break
            
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return heapq.heappop(self.frontier)

    def contains_state(self, state):
        return any(node.state == state for path_cost, node in self.frontier)

    def __str__(self) -> str:
            return str([(path_cost, (node.row, node.column)) for path_cost, node in self.frontier])

class AStarPriorityQueueFrontier(PriorityQueueFrontier):
    def add(self, node, parent_path_cost, grid):
        if not self.contains_state(node.state):  # if node is not already in frontier
            node.path_cost = parent_path_cost + 1
            heapq.heappush(self.frontier, ((parent_path_cost + 1) + grid.get_manhattan_distance_heuristic(node), node))
        else:
            # discard node in frontier if path cost is higher than the current node
            for idx, (cost, frontier_node) in enumerate(self.frontier):
                if frontier_node.state == node.state:
                    if (parent_path_cost + 1) < cost:
                        self.frontier = self.frontier[:idx] + self.frontier[idx + 1:]
                        node.path_cost = parent_path_cost + 1
                        heapq.heappush(self.frontier, ((parent_path_cost + 1) + grid.get_manhattan_distance_heuristic(node), node))
                        break


class GreedyBestFirstPriorityQueueFrontier(PriorityQueueFrontier):
    def add(self, node, grid):
        heuristic_value = grid.get_manhattan_distance_heuristic(node)
        heapq.heappush(self.frontier, (heuristic_value, node))
        # if not self.contains_state(node.state):  # if node is not already in frontier
        #     heapq.heappush(self.frontier, (heuristic_value, node))
        # else:
        #     # discard node in frontier if heuristic is higher than the current node
        #     for idx, (existing_heuristic, frontier_node) in enumerate(self.frontier):
        #         if frontier_node.state == node.state:
        #             if heuristic_value < existing_heuristic:
        #                 self.frontier = self.frontier[:idx] + self.frontier[idx + 1:]  # remove existing node
        #                 heapq.heappush(self.frontier, (heuristic_value, node))
        #                 break