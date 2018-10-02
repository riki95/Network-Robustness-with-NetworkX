import networkx as nx
from random import random
import matplotlib.pyplot as plt
import pylab

from Lab1.analyse_realistic_graph import do_computations

g = nx.DiGraph()


def remove_random_node(g, n=1):
    import random
    for i in range(n):
        node = random.choice(list(g.node.keys()))

        g.remove_node(node)


def create_graph():
    with open('bitcoin.csv') as f:
        for row in f:
            s = row.split(',')
            g.add_edge(s[0], s[1], weight=int(s[2]))


def main():
    g = nx.DiGraph(nx.scale_free_graph(20))
    do_computations(g)
    remove_random_node(g)

    figure = plt.figure()
    # Intact
    G = nx.barabasi_albert_graph(10, 3)

    node_pose = {}
    for i in G.nodes():
        node_pose[i] = (random(), random())

    plt.subplot(121)
    fig1 = nx.draw_networkx(G, pos=node_pose, fixed=node_pose.keys())

    # Two nodes are removed
    e = [4, 6]
    G.remove_nodes_from(e)
    plt.subplot(122)
    fig2 = nx.draw_networkx(G, pos=node_pose, fixed=node_pose.keys())

    plt.show()


if __name__ == '__main__':
    main()