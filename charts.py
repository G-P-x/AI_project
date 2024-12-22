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

def plot_algorithms(algorithms: list[str], execution_times: list[str], nodes_in_fringe: int, nodes_expanded: int, sequence: str):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    bar_width = 0.2
    n = len(algorithms)
    r1 = np.arange(n)
    r2 = [x + bar_width for x in r1]

    # Plotting Execution Time

    ax1.bar(algorithms, execution_times, color='b', width=bar_width, edgecolor='grey', label='Execution Time (s)')
    ax1.set_xlabel('Algorithm', fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontweight='bold')
    ax1.set_title('Execution Time Comparison')
    ax1.legend()

    # Plotting Nodes in Fringe and Expanded
    ax2.bar(r1, nodes_in_fringe, color='r', width=bar_width, edgecolor='grey', label='Nodes in Fringe')
    ax2.bar(r2, nodes_expanded, color='g', width=bar_width, edgecolor='grey', label='Nodes Expanded')
    ax2.set_xlabel('Algorithm', fontweight='bold')
    ax2.set_ylabel('Number of Nodes', fontweight='bold')
    ax2.set_title('Nodes Generated Comparison')
    ax2.set_xticks([r + bar_width/2 for r in range(n)])
    ax2.set_xticklabels(algorithms)
    ax2.legend()
    # Adjust layout
    plt.tight_layout()
    # Show plot
    plt.show()


def plots():
    algoritms = ['A*', 'BFS', 'DFS', 'Greedy', 'UCS']
    execution_time = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]
    expanded_nodes = [10, 20, 30, 40, 50]
    plt.bar(algoritms, execution_time)

    plt.show()

if __name__ == "__main__":
    # plots()
    algoritms = ['A*', 'BFS', 'DFS', 'Greedy', 'UCS']
    execution_time = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]
    nodes_in_fringe = [10, 20, 30, 40, 50]
    expanded_nodes = [10, 60, 40, 50, 60]
    sequence = '102743865'
    plot_algorithms(algoritms, execution_time, nodes_in_fringe, expanded_nodes, sequence)