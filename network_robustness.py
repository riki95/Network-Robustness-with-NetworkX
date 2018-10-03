import networkx as nx
from random import random
import matplotlib.pyplot as plt
import pylab

from Lab1.analyse_realistic_graph import do_computations, create_graph

g = nx.DiGraph()
node_pose = {}


def create_graph():
    with open('bitcoin.csv') as f:
        for row in f:
            s = row.split(',')
            g.add_edge(s[0], s[1], weight=int(s[2]))


def remove_random_node(g, n):
    import random  # This because it crashes against the import at the top which works for the plot
    for i in range(n):
        node = random.choice(list(g.node.keys()))

        g.remove_node(node)
        print("Removed", node)


def draw_graph_fixed(g, ns, fs):
    # Intact graph now
    figure = plt.figure()

    for i in g.nodes():
        node_pose[i] = (random(), random())

    plt.subplot(221)
    fig1 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b', fixed=node_pose.keys())
    plt.savefig('data/' + str('g1') + '.png', dpi=500)


def draw_graph2(g, ns, fs):
    # Two nodes are removed
    plt.subplot(222)
    fig2 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b', fixed=node_pose.keys())
    plt.savefig('data/' + str('g2') + '.png', dpi=500)


def draw_graph3(g, ns, fs):
    # Two nodes are removed
    plt.subplot(223)
    fig3 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b',
                            fixed=node_pose.keys())
    plt.savefig('data/' + str('g3') + '.png', dpi=500)


def draw_graph4(g, ns, fs):
    # Two nodes are removed
    plt.subplot(224)
    fig3 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b',
                            fixed=node_pose.keys())
    plt.savefig('data/' + str('g4') + '.png', dpi=500)


# when you do this remember do compute closeness on analysis
def scale_free_robustness():
    ns = 100
    fs = 8
    g = nx.DiGraph(nx.scale_free_graph(20))
    draw_graph_fixed(g, ns, fs)
    best_node = do_computations(g, 1)

    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 10)
    draw_graph2(g_remove_random, ns, fs)
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    print("Removing best node: " + str(best_node))
    g_remove_most_important.remove_nodes_from([best_node])
    draw_graph3(g_remove_most_important, ns, fs)
    do_computations(g_remove_most_important, 3)

    plt.show()


# when you do this remember do compute degree on analysis
def bitcoin_robustness():
    ns = 50
    fs = 2
    create_graph()
    draw_graph_fixed(g, ns, fs)
    best_node = do_computations(g, 1)

    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 1000)
    draw_graph2(g_remove_random, ns, fs)
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    print("Removing best node: " + str(best_node))
    g_remove_most_important.remove_nodes_from([best_node])
    draw_graph3(g_remove_most_important, ns, fs)
    do_computations(g_remove_most_important, 3)

    best_nodes = [1,2,3,4,7]
    g_remove_most_importants = g.copy()
    print("Removing best nodes: " + str(best_nodes))
    g_remove_most_important.remove_nodes_from(best_nodes)
    draw_graph4(g_remove_most_important, ns, fs)
    do_computations(g_remove_most_important, 4)

    plt.show()


def main():
    scale_free_robustness()
    #bitcoin_robustness()


if __name__ == '__main__':
    main()