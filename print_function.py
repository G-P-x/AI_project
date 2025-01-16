import gc
from problem_definition import Node_8_puzzle

def print_children(children: list[Node_8_puzzle]) -> None:
    '''debugging function to print the children nodes'''
    for child in children:
        print(f"State: {child.state}. Cost: {child.cost}")
    return None

def print_depth_limit_reached(depth: int) -> None:
    print(f"\tDepth limit reached at depth {depth}\n")
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