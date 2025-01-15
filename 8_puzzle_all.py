from counter import Counter
import copy
import time
import charts as ch
import heuristic_functions as h_f_
import gc

class Node_8_puzzle():
    def __init__(self, parent: 'Node_8_puzzle', state: list[list], action: str):
        self.parent = parent  # pointer to the parent node
        self.state = state
        self.n_moves = parent.n_moves + 1 if parent else 0  # this is basically the depth of the node in the tree
        self.action = "root node" if parent is None else action 
        self.cost = 0

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


def set_of_actions(row: int, col: int):
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

def expand_node(node_to_expand: Node_8_puzzle, max_depth) -> list[Node_8_puzzle]:
    '''expands the node and returns 
    -   children nodes with parent, state and action. 
    -   0 if the goal state is reached;
    -   depth limit value if the depth limit is reached'''
    if node_to_expand.state == goal_state:
        return 0
    if node_to_expand.n_moves >= max_depth: # depth limit reached
        return max_depth
    children = []
    b_row, b_col = find_blank_tile(node_to_expand.state)  # find the blank tile
    actions = set_of_actions(b_row, b_col)
    for action in actions:
        child_state = action(node_to_expand, b_row, b_col)
        # check if the child state is already in the path
        if not check_already_visited(child_state, node_to_expand):
            child = Node_8_puzzle(parent=node_to_expand, state=child_state, action=action.__name__)
            if child.n_moves > max_depth:
                continue
                # here I should return something to indicate that the depth limit has been reached
            children.append(child)
    return children

def print_children(children: list[Node_8_puzzle]) -> None:
    '''debugging function to print the children nodes'''
    for child in children:
        print(f"State: {child.state}. Cost: {child.cost}")
    return None

def print_action_sequence(goal_node: Node_8_puzzle) -> None:
    actions = []
    while goal_node.parent != None:
        actions.append(goal_node.action)
        goal_node = goal_node.parent
    actions.reverse()
    print(f"\t{actions}")
    print("\tNumber of moves: ", len(actions))
    return None

def chosen_heuristic(state: list[list[int]], goal: dict):
    # return h_f_.h_3(state, goal)
    # return h_f_.bad_heuristic(state, goal)
    # return h_f_.h_2(state, goal)
    return h_f_.manhattan_distance(goal, state)

def BFS(initial_state: list[list[int]], goal_state: list[list[int]]) -> dict[str: any]:
    '''Breadth-first search algorithm to solve the 8-puzzle, returns a dictionary with the
    'goal_node',
    'expanded_nodes':, 
    'nodes_in_fringe':'''
    counter = Counter()
    root = Node_8_puzzle(parent=None, state=initial_state, action=None)
    fringe = [root]
    counter.expanded_nodes = 0
    max_step = 10
    while fringe:
        node = fringe.pop(0)
        children = expand_node(node_to_expand=node, max_depth=max_step)
        if isinstance(children,int) and children == 0:
            print_memory_usage()
            result = {
                'goal_node': node,
                'expanded_nodes': counter.expanded_nodes,
                'nodes_in_fringe': len(fringe)
            }
            return result
        if isinstance(children, int) and children > 0:
            if fringe == []:
                print(f"\tDepth limit reached at depth {children}\n")
                return None
            continue
        counter.expanded_nodes += 1
        fringe.extend(children)
    print("No solution found within the depth limit of {n}".format(n=max_step))

def limited_DFS(initial_state: list[list[int]], goal_state: list[list[int]], limit = 10) -> dict[str: any]:
    root = Node_8_puzzle(parent=None, state=initial_state, action=None)
    counter = Counter()
    fringe = [root]
    while fringe:
        node = fringe.pop(0)
        counter.expanded_nodes += 1
        children = expand_node(node_to_expand=node, max_depth=limit)
        if isinstance(children, int) and children == 0:
            # goal state reached
            print_memory_usage()
            result = {
                'goal_node': node,
                'expanded_nodes': counter.expanded_nodes,
                'nodes_in_fringe': len(fringe)
            }
            return result
        if isinstance(children, int) and children > 0:
            if fringe == []:
                print(f"\tDepth limit reached at depth {children}\n")
                return None
            continue
        # the garbage collector will remove the nodes that are not needed or referenced
        fringe = children + fringe
    print(f"No solution found within the depth limit of {limit}")

def greedy_search(initial_state: list[list[int]], goal_state: list[list[int]]) -> dict[str: any]:
    '''Greedy search algorithm to solve the 8-puzzle, returns a dictionary with the
    'goal_node',
    'expanded_nodes':, 
    'nodes_in_fringe':'''
    counter = Counter()
    root = Node_8_puzzle(parent=None, state=initial_state, action=None)
    root.cost = chosen_heuristic(initial_state, goal_dict)
    # root = Node_8_puzzle(None, initial_state, heuristic_manhattan_distance(initial_state, goal_dict), None)
    
    # create a list to store the nodes that have not been expanded yet
    fringe = [root]
    counter.expanded_nodes = 0

    while fringe:
        node = min(fringe, key=lambda x: x.cost)
        fringe.remove(node) # remove the node selected for expansion from the fringe
        # print(f"Node {node.state}, cost: {node.approx_cost}")
        # expand the node
        children = expand_node(node_to_expand=node, max_depth=30)  
        if isinstance(children, int) and children == 0:
            print_memory_usage()
            # node is the result
            result = {
                'goal_node': node,
                'expanded_nodes': counter.expanded_nodes,
                'nodes_in_fringe': len(fringe)
            }
            return result   
        if isinstance(children, int) and children > 0:
            if fringe == []:
                print(f"\tDepth limit reached at depth {children}\n")
                return None
            continue
        counter.expanded_nodes += 1  # increment the number of expanded nodes
        # compute the heuristic value for each child
        for child in children:
            child.cost = chosen_heuristic(child.state, goal_dict)
        fringe.extend(children)
    print(f"No solution found whitin the depth limit of 30")

def A_star(initial_state: list[list[int]], goal_state: list[list[int]]) -> dict[str: any]:
    '''A* algorithm to solve the 8-puzzle, returns a dictionary with the
    'goal_node',
    'expanded_nodes':, 
    'nodes_in_fringe':'''
    counter = Counter()
    root = Node_8_puzzle(parent=None, state=initial_state, action=None)
    root.cost = chosen_heuristic(initial_state, goal_dict) + root.n_moves
    # root = Node_8_puzzle(None, initial_state, heuristic_manhattan_distance(initial_state, goal_dict), None)
    
    # create a list to store the nodes that have not been expanded yet
    fringe = [root]
    counter.expanded_nodes = 0

    while fringe:
        # sort the fringe based on the path cost + heuristic value
        # fringe.sort(key=lambda x: x.approx_cost) # increse the time complexity
        # pop the node with the lowest cost
        # fringe.pop(0)

        node = min(fringe, key=lambda x: x.cost)
        fringe.remove(node) # remove the node selected for expansion from the fringe
        # print(f"Node {node.state}, cost: {node.approx_cost}")
        # expand the node
        children = expand_node(node_to_expand=node, max_depth=30)  

        # check if the goal state has been reached
        if isinstance(children, int) and children == 0:
            print_memory_usage()
            # node is the result
            result = {
                'goal_node': node,
                'expanded_nodes': counter.expanded_nodes,
                'nodes_in_fringe': len(fringe)
            }
            return result
        if isinstance(children, int) and children > 0:
            if fringe == []:
                print(f"\tDepth limit reached at depth {children}\n")
                return None
            continue
        counter.expanded_nodes += 1  # increment the number of expanded nodes
        # compute the heuristic value for each child + the number of moves 
        for child in children:
            child.cost = chosen_heuristic(child.state, goal_dict) + child.n_moves   
        fringe.extend(children)
    #print(f"No solution found whitin the depth limit of 30")

def create_matrix(values: str):
    assert len(values) == 9, "The length of the sequence must be 9"
    matrix = []
    for i in range(0, len(values), 3):
        matrix.append([int(values[i]), int(values[i+1]), int(values[i+2])])
    return matrix

def print_results(result: dict[str: any], finish_time) -> None:
    '''print the results of the search algorithm'''
    print(f"\tExpanded nodes: {result['expanded_nodes']}. Nodes in fringe: {result['nodes_in_fringe']}")
    print("\tExecution time: {:.8f} milliseconds".format(finish_time * 1000))
    print_action_sequence(goal_node=result['goal_node'])
    return None

def print_memory_usage() -> None:
    objects_in_memory = [obj for obj in gc.get_objects() if isinstance(obj, Node_8_puzzle)]
    print(f"\tnodes in memory: {len(objects_in_memory)}" )
    return None

if __name__ == "__main__":
    start_sequences = [
    '102743865',
    '328407615',
    '513824076',
    '142807365',
    '281503476',
    '561702438',
    ]
    assert create_matrix('102743865') == [[1, 0, 2], [7, 4, 3], [8, 6, 5]]
    assert create_matrix('328407615') == [[3, 2, 8], [4, 0, 7], [6, 1, 5]]
    start_sequence = create_matrix('102743865')
    goal_dict = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
    }  # used to calculate the heuristic value
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    times = []
    algorithms = [greedy_search, A_star, limited_DFS, BFS]
    i = 0
    if i == 0:
        # here I cannot use the memory profiler because it will not work with the garbage collector 
        # since I'm keeping references to the nodes in the results list
        results = []
        for s in start_sequences:
            print(f"Start sequence: {s}")
            for algorithm in algorithms:
                print(f"\n\tAlgorithm: {algorithm.__name__}")
                start_time = time.time()
                result = algorithm(create_matrix(s), goal_state)
                if result is not None:
                    times.append(time.time() - start_time)
                    results.append(result)
                    print_results(result, times[-1])
                    print("\n")
    elif i == 1:
        print("\n\nStart sequence: 812574063")
        for algorithm in algorithms:
            print(f"\n\tAlgorithm: {algorithm.__name__}")        
            start_time = time.time()
            result = algorithm(create_matrix('812574063'), goal_state)
            print_results(result, time.time() - start_time)
            result = None # remove the reference to the result otherwise it will not be deleted by the garbage collected
            # Some programs manage large amounts of data or create temporary objects 
            # that consume significant memory.
            # If result is not explicitly set to None (or some other non-referencing value), 
            # the reference to the object remains, 
            # preventing Python from reclaiming the memory used by the object.
    else:
        print("\n\nStart sequence: 120453786: goal = 102453786")
        goal_state = [[1, 0, 2], [4, 5, 3], [7, 8, 6]]
        print
        start_sequence = create_matrix('120453786')
        start_time = time.time()
        result = limited_DFS(start_sequence, goal_state)
        print_results(result, time.time() - start_time)

    
    # ch.plot_sequence_results_A_star(start_sequences, times, [r['nodes_in_fringe'] for r in results], [r['expanded_nodes'] for r in results])