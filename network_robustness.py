import networkx as nx
import random
import analyse_realistic_graph.py as ga
import matplotlib.pyplot as plt


def remove_random_node(g, pos, name, n=1):
    for i in range(n):
        node = random.choice(list(g.node.keys()))

        g.remove_node(node)

        show(g, pos, '{} rand {}'.format(name, i))


def show(g, pos, name):
    ga.file = open('prova', 'w')

    ga.compute_trust(g)

    if pos is not None:
        nx.draw(g, pos=pos)
        plt.draw()
        plt.show()
        plt.savefig('gprova.png'.format(name), dpi=500)
        plt.close()

    ga.file.close()


def main():
    g = nx.DiGraph(nx.scale_free_graph(20))
    print()


if __name__ == '__main__':
    main()