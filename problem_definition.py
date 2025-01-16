import copy

class Node_8_puzzle():
    def __init__(self, parent: 'Node_8_puzzle', state: list[list], action: str):
        self.parent = parent  # pointer to the parent node
        self.state = state
        self.n_moves = parent.n_moves + 1 if parent else 0  # this is basically the depth of the node in the tree
        self.action = "root node" if parent is None else action 
        self.cost = 0

## Action functions
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

# maybe, this function should be in the 8_puzzle_all.py file since it is mostly
# releated to the algorithm and not the problem definition
def check_already_visited(state: list[list[int]], parent: Node_8_puzzle):
    while parent != None:
        if parent.state == state:
            return True
        parent = parent.parent
    return False

def find_blank_tile(state: list[list[int]]):
    '''return the row and column of the blank tile'''
    for l in state:
        if 0 in l:
            row = state.index(l)
            col = l.index(0)
            break
    return row, col

def set_of_actions(row: int, col: int):
    '''return the set of actions that can be taken from the current state'''
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
