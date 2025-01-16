from counter import Counter
import copy
import time
import charts as ch
import heuristic_functions as h_f_
import gc
import print_function as pf
from problem_definition import Node_8_puzzle
import problem_definition as act

def check_already_visited(state: list[list[int]], parent: Node_8_puzzle):
    '''check if the state is already in the path before creating a new node'''
    while parent != None:
        if parent.state == state:
            return True
        parent = parent.parent
    return False

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
    b_row, b_col = act.find_blank_tile(node_to_expand.state)  # find the blank tile
    actions = act.set_of_actions(b_row, b_col)
    for action in actions:
        child_state = action(node_to_expand, b_row, b_col)
        # check if the child state is already in the path
        if not act.check_already_visited(child_state, node_to_expand):
            child = Node_8_puzzle(parent=node_to_expand, state=child_state, action=action.__name__)
            if child.n_moves > max_depth:
                continue
                # here I should return something to indicate that the depth limit has been reached
            children.append(child)
    return children

def standardise_result(node: Node_8_puzzle, counter, fringe) -> list[str]:
    result = {
        'goal_node': node,
        'expanded_nodes': counter.expanded_nodes,
        'nodes_in_fringe': len(fringe)
    }
    return result

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
            return standardise_result(node, counter, fringe)
        if isinstance(children, int) and children > 0:
            if fringe == []:
                pf.print_depth_limit_reached(children)
                result = {
                    'goal_node': None,
                    'expanded_nodes': counter.expanded_nodes,
                    'nodes_in_fringe': len(fringe)
                }
                return result
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
            return standardise_result(node, counter, fringe)
        if isinstance(children, int) and children > 0:
            if fringe == []:
                pf.print_depth_limit_reached(children)
                result = {
                    'goal_node': None,
                    'expanded_nodes': counter.expanded_nodes,
                    'nodes_in_fringe': len(fringe)
                }
                return result
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
            return standardise_result(node, counter, fringe) 
        if isinstance(children, int) and children > 0:
            if fringe == []:
                pf.print_depth_limit_reached(children)
                result = {
                    'goal_node': None,
                    'expanded_nodes': counter.expanded_nodes,
                    'nodes_in_fringe': len(fringe)
                }
                return result
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
            return standardise_result(node, counter, fringe)
        if isinstance(children, int) and children > 0:
            if fringe == []:
                return pf.print_depth_limit_reached(children)
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

# must stay in the same file as the functions that use it otherwise it will not work
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
                results.append(result)
                if result["goal_node"] is not None:
                    times.append(time.time() - start_time)
                    pf.print_results(result, times[-1])
                    print("\n")
        i = 0
        for s in start_sequences:
            expanded_nodes = [r['expanded_nodes'] for r in results][i: i + len(algorithms)]
            str_algorithms = [al.__name__ for al in algorithms]
            ch.plot_algorithms_computational_complexity(str_algorithms, expanded_nodes, s)
            i+= len(algorithms)
            
    elif i == 1:
        print("\n\nStart sequence: 812574063")
        for algorithm in algorithms:
            print(f"\n\tAlgorithm: {algorithm.__name__}")        
            start_time = time.time()
            result = algorithm(create_matrix('812574063'), goal_state)
            pf.print_results(result, time.time() - start_time)
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
        pf.print_results(result, time.time() - start_time)

    
    # ch.plot_sequence_results_A_star(start_sequences, times, [r['nodes_in_fringe'] for r in results], [r['expanded_nodes'] for r in results])