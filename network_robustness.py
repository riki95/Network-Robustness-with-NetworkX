import networkx as nx
import random
import matplotlib.pyplot as plt

from Lab1.analyse_realistic_graph import do_computations


def remove_random_node(g, n=1):
    for i in range(n):
        node = random.choice(list(g.node.keys()))

        g.remove_node(node)

        draw_graph(g)


def draw_graph(g):
    nx.draw_networkx(g, node_size=50, font_size=2, arrowsize=3, node_color='b')
    plt.draw()
    plt.show()


def main():
    g = nx.DiGraph(nx.scale_free_graph(20))
    do_computations(g)
    draw_graph(g)
    remove_random_node(g)
    do_computations(g)


if __name__ == '__main__':
    main()