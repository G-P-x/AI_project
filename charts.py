import matplotlib.pyplot as plt
import numpy as np

def plot_algorithms_over_time(algorithms: list[str], execution_times, nodes_in_fringe, nodes_expanded, sequence: str):
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
    plot_algorithms_over_time(algoritms, execution_time, nodes_in_fringe, expanded_nodes, sequence)