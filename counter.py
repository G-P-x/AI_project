class Counter:
    def __init__(self):
        self.total_nodes = 0
        self.expanded_nodes = 0
        self.fringe_nodes = 0

    def increment_total_nodes(self, n: int):
        self.total_nodes += n

    def increment_expanded_nodes(self, n: int):
        self.expanded_nodes += n

    def increment_fringe_nodes(self, n: int):
        self.fringe_nodes += n