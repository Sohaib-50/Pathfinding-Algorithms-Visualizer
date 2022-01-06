class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
            # return self.frontier.pop()
    
    def reset(self):
        self.frontier = []
        
    def __str__(self) -> str:
        coordinates = [(node.row, node.column) for node in self.frontier]
        return str(coordinates)

    def __len__(self) -> int:
        return len(self.frontier)


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            # return self.frontier.pop(0)
            node = self.frontier[0]
            # self.frontier = self.frontier[1:]
            self.frontier.pop(0)
            return node
