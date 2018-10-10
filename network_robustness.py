import networkx as nx
from random import random
import matplotlib.pyplot as plt
import pylab

from Lab1.analyse_realistic_graph import do_computations, create_graph, compute_centrality, draw_graph

g = nx.DiGraph()
node_pose = {}
plotOn = False
drawGraphOn = True


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


def draw_graph(g, layout, title, nameFile):
    plt.title(title)
    nx.draw_networkx(g, node_size=50, font_size=6, arrowsize=3, node_color='b', pos=layout)
    plt.savefig('data/' + nameFile + '.png', dpi=500)
    plt.show()


def draw_graph_fixed(g, ns, fs):
    # Intact graph now
    figure = plt.figure()

    for i in g.nodes():
        node_pose[i] = (random(), random())

    plt.subplot(221)
    fig1 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b',
                            fixed=node_pose.keys())
    plt.savefig('data/' + str('g1') + '.png', dpi=500)


def draw_graph2(g, ns, fs):
    # Two nodes are removed
    plt.subplot(222)
    fig2 = nx.draw_networkx(g, pos=node_pose, node_size=ns, font_size=fs, arrowsize=3, node_color='b',
                            fixed=node_pose.keys())
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
    g = nx.DiGraph(nx.scale_free_graph(20)).to_undirected()

    print("Graph")
    fixed_positions = {1: (0, 0), 2: (-1, 2)}  # dict with two of the positions set
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(g, pos=fixed_positions, fixed=fixed_nodes)

    if drawGraphOn:
        draw_graph(g, pos, "Graph", '1')
    best_node = do_computations(g, 1)

    print("Graph with 10 random nodes removed")
    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 10)
    if drawGraphOn:
        draw_graph(g_remove_random, pos, "Graph with 10 random nodes removed", '2')
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    for x in range(2):
        best_node = compute_centrality(g_remove_most_important)
        print("Removed best node: " + str(best_node))
        g_remove_most_important.remove_nodes_from([best_node])
        if drawGraphOn:
            draw_graph(g_remove_most_important, pos, "Graph with node " + str(best_node) + "removed", str(x+3))
        do_computations(g_remove_most_important, 3)


    plt.show()


# when you do this remember do compute degree on analysis
def bitcoin_robustness():
    ns = 50
    fs = 2
    create_graph()
    if drawGraphOn:
        draw_graph(g)
    best_node = do_computations(g, 1)

    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 1000)
    if drawGraphOn:
        draw_graph(g_remove_random)
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    print("Removing best node: " + str(best_node))
    g_remove_most_important.remove_nodes_from([best_node])
    if drawGraphOn:
        draw_graph(g_remove_most_important)
    do_computations(g_remove_most_important, 3)

    best_nodes = [1,2,3,4,7]
    g_remove_most_importants = g.copy()
    print("Removing best nodes: " + str(best_nodes))
    g_remove_most_importants.remove_nodes_from(best_nodes)
    if drawGraphOn:
        draw_graph(g_remove_most_importants)
    do_computations(g_remove_most_importants, 4)

    plt.show()


def main():
    scale_free_robustness()
    #bitcoin_robustness()


if __name__ == '__main__':
    main()