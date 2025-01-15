def h1(goal: dict, state: list) -> int:
    '''Not admissible heuristic function'''
    assert isinstance(goal, dict), "goal must be a dictionary"
    assert isinstance(state, list), "state must be a list"

    distance = 0
    total_distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col] # get the integer value of the tile
            distance = abs(row - goal[tile][0]) + abs(col - goal[tile][1])
            if distance > 1:
                distance *= 2
            total_distance += distance

def manhattan_distance(goal: dict, state: list) -> int:
    '''Manhattan distance heuristic function'''
    assert isinstance(goal, dict), "goal must be a dictionary"
    assert isinstance(state, list), "state must be a list"
    distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            distance += abs(row - goal[tile][0]) + abs(col - goal[tile][1])
    return distance

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

def h_2(state: list[list[int]], goal: dict):
    '''Unadmissible heuristic function'''
    # calculate the number of moves that each tile is from its goal position
    # for each tile in the current state, calculate the manhattan distance to its goal position
    # sum all the distances to get the heuristic value

    #just find out that also this one is not admissible, 812574063 gets 22 moves instead of 20.
    assert isinstance(goal, dict), "goal must be a dictionary"
    assert isinstance(state, list), "state must be a list"
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

def bad_heuristic(state: list[list[int]], goal: dict):
    distance = 0
    total_distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col] # get the integer value of the tile
            if tile != 0:
                distance = abs(row - goal[tile][0]) + abs(col - goal[tile][1])
                if distance > 1:
                    distance *= 0.5 # from 1.4 onwards, the heuristic is not admissible for sure
                total_distance += distance
    return total_distance

def h_3(state: list[list[int]], goal: dict):
    '''Count the number of misplaced tiles'''
    assert isinstance(goal, dict), "goal must be a dictionary"
    assert isinstance(state, list), "state must be a list"
    count = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            if tile != 0 and tile != goal[tile]:
                count += 1
    return count
