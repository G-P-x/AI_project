from counter import Counter
import copy
import time

class Node_8_puzzle():
    def __init__(self, parent: 'Node_8_puzzle', state: list[list], heuristic, action: str):
        self.parent = parent  # pointer to the parent node
        self.state = state
        self.n_moves = parent.n_moves + 1 if parent else 0
        self.approx_cost = heuristic + self.n_moves
        self.action = "root node" if parent is None else action 

def heuristic_manhattan_distance(state: list[list[int]], goal: dict) -> int:
    assert isinstance(goal, dict), "goal must be a dictionary"
    assert isinstance(state, list), "state must be a list"
    distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            if tile != 0:
                distance += abs(row - goal[tile][0]) + abs(col - goal[tile][1])
    return distance

def compute_heuristic_1(state: list[list[int]], goal: dict):
        # calculate the number of moves that each tile is from its goal position
        # for each tile in the current state, calculate the manhattan distance to its goal position
        # sum all the distances to get the heuristic value
        distance = 0
        total_distance = 0
        for row in range(3):
            for col in range(3):
                tile = state[row][col] # get the integer value of the tile
                if tile != 0:
                    distance = abs(row - goal[tile][0]) + abs(col - goal[tile][1])
                    if distance > 1:
                        distance *= 1.4 # from 1.4 onwards, the heuristic is not admissible for sure
                    total_distance += distance
        return total_distance

def find_blank_tile(state: list[list[int]]):
    for l in state:
        if 0 in l:
            row = state.index(l)
            col = l.index(0)
            break
    return row, col

def check_if_node_in_path(node: Node_8_puzzle):
    '''check if the node is already in the path'''
    while node.parent != None:
        if node.parent.state == node.state:
            return True
        node = node.parent
    return False

def check_already_visited(state: list[list[int]], parent: Node_8_puzzle):
    while parent != None:
        if parent.state == state:
            return True
        parent = parent.parent
    return False

def up(node_up: Node_8_puzzle, row: int, col: int):
    '''swap the blank tile with the tile above it'''
    new_state = copy.deepcopy(node_up.state)
    new_state[row][col] = new_state[row - 1][col]
    new_state[row-1][col] = node_up.state[row][col]
    return new_state

def down(node_down: Node_8_puzzle, row: int, col: int):
    '''swap the blank tile with the tile below it'''
    new_state = copy.deepcopy(node_down.state)
    new_state[row][col] = new_state[row + 1][col]
    new_state[row+1][col] = node_down.state[row][col]
    return new_state

def left(node_left: Node_8_puzzle, row: int, col: int):
    '''swap the blank tile with the tile to the left of it'''
    new_state = copy.deepcopy(node_left.state)
    new_state[row][col] = new_state[row][col - 1]
    new_state[row][col-1] = node_left.state[row][col]
    return new_state

def right(node_right: Node_8_puzzle, row: int, col: int):
    '''swap the blank tile with the tile to the right of it'''
    new_state = copy.deepcopy(node_right.state)
    new_state[row][col] = new_state[row][col + 1]
    new_state[row][col+1] = node_right.state[row][col]
    return new_state


def set_of_actions(node: Node_8_puzzle, row: int, col: int):
    actions = []
    if row > 0:
        actions.append(up)
    if row < 2:
        actions.append(down)
    if col > 0:
        actions.append(left)
    if col < 2:
        actions.append(right)
    return actions

def expand_node(node_to_expand: Node_8_puzzle):
    if node_to_expand.state == goal_state:
        return None
    children = []
    b_row, b_col = find_blank_tile(node_to_expand.state)  # find the blank tile
    actions = set_of_actions(node_to_expand, b_row, b_col)
    for action in actions:
        child_state = action(node_to_expand, b_row, b_col)
        # check if the child state is already in the path
        if not check_already_visited(child_state, node_to_expand):
            child = Node_8_puzzle(node_to_expand, child_state, chosen_heuristic(child_state, goal_dict), action.__name__)
            # child = Node_8_puzzle(node_to_expand, child_state, heuristic_manhattan_distance(child_state, goal_dict), action.__name__)
            if child.n_moves > 30:
                continue
            children.append(child)
    # print_children(children)
    return children

def print_children(children: list[Node_8_puzzle]) -> None:
    for child in children:
        print(f"State: {child.state}. Cost: {child.approx_cost}")
    return None

def print_action_sequence(goal_node: Node_8_puzzle) -> None:
    actions = []
    while goal_node.parent != None:
        actions.append(goal_node.action)
        goal_node = goal_node.parent
    actions.reverse()
    print(actions)
    print("Number of moves: ", len(actions))
    return None

def chosen_heuristic(state: list[list[int]], goal: dict):
    return compute_heuristic_1(state, goal)
    return heuristic_manhattan_distance(state, goal)

def A_star(initial_state: list[list[int]], goal_state: list[list[int]]):
    counter = Counter()
    root = Node_8_puzzle(None, initial_state, chosen_heuristic(initial_state, goal_dict), None)
    # root = Node_8_puzzle(None, initial_state, heuristic_manhattan_distance(initial_state, goal_dict), None)
    
    # create a list to store the nodes that have not been expanded yet
    fringe = [root]
    counter.expanded_nodes = 0

    while fringe:
        # sort the fringe based on the path cost + heuristic value
        # fringe.sort(key=lambda x: x.approx_cost)
        # pop the node with the lowest cost
        # fringe.pop(0)

        node = min(fringe, key=lambda x: x.approx_cost)
        fringe.remove(node)
        # print(f"Node {node.state}, cost: {node.approx_cost}")
        # expand the node
        children = expand_node(node_to_expand=node)      
        # check if the goal state has been reached
        if children == None:
            # print the result
            print_action_sequence(goal_node=node)
            print("Number of nodes expanded: ", counter.expanded_nodes)
            print("Node in the fringe: ", len(fringe))
            return    
        counter.expanded_nodes += 1     
        fringe.extend(children)
    print(f"No solution found whitin the depth limit of 30")

def create_matrix(values: str):
    assert len(values) == 9, "The length of the sequence must be 9"
    matrix = []
    for i in range(0, len(values), 3):
        matrix.append([int(values[i]), int(values[i+1]), int(values[i+2])])
    return matrix

if __name__ == "__main__":
    # initial state of the 8-puzzle
    start_sequences = {
        1: '102743865', # solution at depth 9
        2: '328407615', # solution at depth 28
        3: '513824076', # solution at depth 16
        4: '142807365', # solution at depth 20
        5: '281503476', # solution at depth 16
    }
    assert create_matrix('102743865') == [[1, 0, 2], [7, 4, 3], [8, 6, 5]]
    assert create_matrix('328407615') == [[3, 2, 8], [4, 0, 7], [6, 1, 5]]
    start_sequence = create_matrix('328407615')
    goal_dict = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
    }  # used to calculate the heuristic value

    # goal state of the 8-puzzle
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    # A_star(start_sequence, goal_state)
    for s in start_sequences:
        print(f"Start sequence: {start_sequences[s]}")
        start_time = time.time()
        A_star(create_matrix(start_sequences[s]), goal_state)
        print("Execution time: {:.5f} seconds".format(time.time() - start_time))
        print("\n")