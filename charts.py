import matplotlib.pyplot as plt
import numpy as np

def plot_alogrithms_over_time(algorithms: list[str], execution_times: list[str], nodes_in_fringe: int, nodes_expanded: int, sequence: str):
    # setup the plot
    n = len(algorithms)
    if n%2 == 0:
        fig, axis = plt.subplots(int(n/2), 2, figsize=(10, 10))
    else:
        fig, axis = plt.subplots(int(n/2) + 1, 2, figsize=(10, 10)) 
    bar_width = 0.2
    x_points = np.arange(n)

    for ax in axis:
        ax.bar(algorithms, execution_times, color='b', width=bar_width, edgecolor='grey', label='Execution Time (s)')
    # Adjust layout
    plt.tight_layout()
    # Show plot
    plt.show()

def plot_sequence_results_A_star(sequences: list[str], execution_times: list[float], nodes_in_fringe: list[int], nodes_expanded: list[int]):
    '''Confronts the results of the A* algorithm for different sequences with respect to the execution time, nodes in fringe and nodes expanded'''
    # setup the plot
    fig, axis = plt.subplots(3, 1, figsize=(10, 10))        
    bar_width = 0.2
    axis[0].bar(sequences, execution_times, color='b', width=bar_width, edgecolor='grey', label='Execution Time (s)')
    axis[0].set_xlabel('Sequence', fontweight='bold')
    axis[0].set_ylabel('Time (seconds)', fontweight='bold')
    axis[0].set_title('Execution Time Comparison')
    axis[0].legend()

    axis[1].bar(sequences, nodes_in_fringe, color='r', width=bar_width, edgecolor='grey', label='Nodes in Fringe')
    axis[1].set_xlabel('Sequence', fontweight='bold')
    axis[1].set_ylabel('Nodes in Fringe', fontweight='bold')
    axis[1].set_title('Nodes in Fringe Comparison')
    axis[1].legend()

    axis[2].bar(sequences, nodes_expanded, color='g', width=bar_width, edgecolor='grey', label='Nodes Expanded')
    axis[2].set_xlabel('Sequence', fontweight='bold')
    axis[2].set_ylabel('Expanded Nodes', fontweight='bold')
    axis[2].set_title('Nodes Expanded Comparison')
    axis[2].legend()
    # Adjust layout
    plt.tight_layout()
    # Show plot
    plt.show()

def plot_algorithms_computational_complexity(algorithms: list[str], expanded_nodes: list[int], sequence: str):
    '''Plots the computational complexity of the algorithms in terms nodes expanded'''
    assert isinstance(algorithms, list), "algorithms must be a list"
    assert len(algorithms) == 4, "algorithms must have 4 elements"
    assert len(expanded_nodes) == 4, "expanded_nodes must have 4 elements"
    assert isinstance(expanded_nodes, list), "expanded_nodes must be a list"
    assert len(algorithms) == len(expanded_nodes), "algorithms and expanded_nodes must have the same length"
    assert isinstance(sequence, str), "sequence must be a string"
    plt.bar(algorithms, expanded_nodes, color='b', width=0.2, align="center", edgecolor='grey', label='Nodes Expanded')
    plt.xlabel('Algorithm', fontweight='bold')
    plt.ylabel('Node Expanded', fontweight='bold')
    plt.title(f'Computational Complexity Comparison: {sequence}')
    # plt.legend()
    # Adjust layout
    plt.tight_layout()
    # Show plot
    plt.show()

def plot_algorithms_memory_usage(algorithms: list[str], nodes_in_fringe: int, nodes_expanded: int, sequence: str):
    '''Plots the memory usage of the algorithms in terms nodes expanded'''
    pass

if __name__ == "__main__":
    # plots()
    algoritms = ['A*', 'BFS', 'limited_DFS', 'Greedy']
    # execution_time = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]
    sequences = ['102743865', '102743865', '102743865']
    for s in sequences:
        nodes_in_fringe = [10, 20, 30, 40, 50]
        expanded_nodes = [10, 60, 40, 50]
        sequence = s
        plot_algorithms_computational_complexity(algoritms, expanded_nodes, sequence)