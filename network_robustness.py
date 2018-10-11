import matplotlib.pyplot as plt
import networkx as nx
import heapq


from Lab1.analyse_realistic_graph import do_computations, create_graph, compute_centrality

g = nx.Graph().to_undirected()
node_pose = {}
drawGraphOn = False


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


def draw_graph(g, layout, title, namefile):
    plt.title(title)
    if g.number_of_nodes() < 100:
        nx.draw_networkx(g, node_size=150, font_size=9, arrowsize=3, node_color='b', pos=layout)
    else:
        nx.draw_networkx(g, node_size=50, font_size=6, arrowsize=3, node_color='b', pos=layout)
    plt.savefig('data/' + namefile + '.png', dpi=500)
    plt.close()


# when you do this remember do compute closeness on analysis
def scale_free_robustness():
    g = nx.DiGraph(nx.scale_free_graph(20)).to_undirected()

    fixed_positions = {1: (0, 0), 2: (-1, 2)}  # dict with two of the positions set
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(g, pos=fixed_positions, fixed=fixed_nodes)

    print("Graph")
    if drawGraphOn:
        draw_graph(g, pos, "Graph", 'g1')
    do_computations(g, 1)

    print("Graph with 10 random nodes removed")
    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 10)
    if drawGraphOn:
        draw_graph(g_remove_random, pos, "Graph with 10 random nodes removed", 'g2')
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    for x in range(4):
        best_node = compute_centrality(g_remove_most_important)
        print("Removed best node: " + str(best_node))
        g_remove_most_important.remove_nodes_from([best_node])
        if drawGraphOn:
            draw_graph(g_remove_most_important, pos, "Graph with node " + str(best_node) + " removed", 'g' + str(x+3))
        do_computations(g_remove_most_important, x+3)


# when you do this remember do compute degree on analysis
def bitcoin_robustness():
    create_graph()
    g.to_undirected()
    pos = nx.spring_layout(g)

    print("Graph")
    if drawGraphOn:
        draw_graph(g, pos, "Bitcoin Graph", 'g1')
    do_computations(g, 1)

    g_remove_random = g.copy()
    remove_random_node(g_remove_random, 1000)
    if drawGraphOn:
        draw_graph(g_remove_random, pos, "Graph with 1000 random removed", 'g2')
    do_computations(g_remove_random, 2)

    g_remove_most_important = g.copy()
    for x in range(20):
        best_node = compute_centrality(g_remove_most_important)
        print("Removed best node: " + str(best_node))
        g_remove_most_important.remove_nodes_from([best_node])

        draw_graph(g_remove_most_important, pos, "Graph with node " + str(best_node) + " removed",
                   'g' + str(x + 3))
        do_computations(g_remove_most_important, x + 3)

    for x in range(980):
        best_node = compute_centrality(g_remove_most_important)
        print("Removed best node: " + str(best_node))
        g_remove_most_important.remove_nodes_from([best_node])

    draw_graph(g_remove_most_important, pos, "Graph with node " + str(best_node) + " removed",
               'g' + str(x + 3))
    do_computations(g_remove_most_important, x + 3)


def bitcoin_robustness2():
    create_graph()
    g.to_undirected()
    pos = nx.spring_layout(g)

    g_remove_most_important = g.copy()
    list_components = []
    list_removed = []
    list_diameters = []
    list_diameters_number = []
    list_diameters_max = []
    list_diameters_min = []

    comps = list(nx.connected_component_subgraphs(g_remove_most_important))
    comp_len = len(comps)
    diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
    list_diameters_max.append(max(diameters))
    list_diameters_min.append(min(diameters))
    list_diameters.append(sum(diameters) / len(diameters))
    list_diameters_number.append(0)

    for x in range(1000):
        best_node = compute_centrality(g_remove_most_important, 'degree')
        g_remove_most_important.remove_nodes_from([best_node])

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        comp_len = len(comps)
        if x == 10 or x==20 or x==30 or x==40 or x==50 or x==60 or x==70 or x==80 or x==90 or x==100 or x==200 \
                or x==300 or x==400 or x==500 or x==600 or x==700 or x==900 or x==1000:
            diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
            list_diameters_max.append(max(diameters))
            list_diameters_min.append(min(diameters))
            list_diameters.append(sum(diameters) / len(diameters))
            list_diameters_number.append(x)
        list_components.append(comp_len)
        list_removed.append(x)

    plt.plot(list_removed, list_components, 'r-')
    plt.ylabel("Components")
    plt.xlabel("Removed")
    plt.legend(['Components', 'Diameters Max', 'Diameters Min', 'Diameters avg'], loc='upper right')
    plt.show()


def bitcoin_robustness3():
    create_graph()
    g.to_undirected()
    pos = nx.spring_layout(g)

    g_remove_most_important = g.copy()
    list_components = []
    list_removed = []
    list_removed2 = [100,200,300,400,500,600,700,800,900,1000]
    list_diameters = []
    list_diameters_number = []
    list_diameters_max = []
    list_diameters_min = []
    list_giantcomponentnodes = []

    print("::: Computing Degree :::")
    for x in range(1000):
        best_node, nodes = compute_centrality(g_remove_most_important, 'degree')

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()
        comp_len = len(comps)

        if x == 10 or x == 100 or x == 200 or x == 300 or x == 400 or x == 500 or x == 600 or x == 700 or x == 900 \
                or x == 1000:
            diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
            list_diameters_max.append(max(diameters))
            list_diameters_min.append(min(diameters))
            list_diameters.append(sum(diameters) / len(diameters))
            list_diameters_number.append(x)
            list_giantcomponentnodes.append(comp_nodes_number)

        list_components.append(comp_len)
        list_removed.append(x)

        g_remove_most_important.remove_nodes_from([best_node])

    g_remove_most_important = g.copy()
    list_components2 = []
    list_giantcomponentnodes2 = []
    list_diameters2 = []
    list_diameters_number2 = []
    list_diameters_max2 = []
    list_diameters_min2 = []

    print("::: Computing Closeness :::")
    for x in range(10):
        best_node, nodes = compute_centrality(g_remove_most_important, 'closeness')
        first_nodes = heapq.nlargest(100, nodes, key=nodes.get)

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        comp_len = len(comps)
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()

        diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
        list_diameters_max2.append(max(diameters))
        list_diameters_min2.append(min(diameters))
        list_diameters2.append(sum(diameters) / len(diameters))
        list_diameters_number2.append(x)

        list_giantcomponentnodes2.append(comp_nodes_number)
        list_components2.append(comp_len)

        g_remove_most_important.remove_nodes_from(first_nodes)

    g_remove_most_important = g.copy()
    list_components3 = []
    list_giantcomponentnodes3 = []
    list_diameters3 = []
    list_diameters_number3 = []
    list_diameters_max3 = []
    list_diameters_min3 = []

    print("::: Computing Betweenness :::")
    for x in range(10):
        best_node, nodes = compute_centrality(g_remove_most_important, 'betweenness')
        first_nodes = heapq.nlargest(100, nodes, key=nodes.get)

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        comp_len = len(comps)
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()

        diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
        list_diameters_max3.append(max(diameters))
        list_diameters_min3.append(min(diameters))
        list_diameters3.append(sum(diameters) / len(diameters))
        list_diameters_number3.append(x)

        list_giantcomponentnodes3.append(comp_nodes_number)
        list_components3.append(comp_len)

        g_remove_most_important.remove_nodes_from(first_nodes)

    print("::: Plotting :::")
    # Plot of different centrality algo
    plt.plot(list_removed, list_components, 'r-')
    plt.plot(list_removed2, list_components2, 'b-')
    plt.plot(list_removed2, list_components3, 'g-')
    plt.ylabel("Components number")
    plt.xlabel("Removed nodes")
    plt.legend(['Degree', 'Closeness', 'Betweenness'], loc='lower right')
    plt.savefig('data/' + 'centralitiescomponents' + '.png', dpi=500)
    plt.show()

    # Plot of Giant Component nodes number
    plt.plot(list_diameters_number, list_giantcomponentnodes, 'r-')
    plt.plot(list_removed2, list_giantcomponentnodes2, 'b-')
    plt.plot(list_removed2, list_giantcomponentnodes3, 'g-')
    plt.ylabel("Giant Component number of nodes")
    plt.xlabel("Removed nodes")
    plt.legend(['Degree', 'Closeness', 'Betweenness'], loc='lower right')
    plt.savefig('data/' + 'giantcomponents' + '.png', dpi=500)
    plt.show()

    # Plot of degree diameters
    plt.plot(list_diameters_number, list_diameters_max, 'r-')
    plt.plot(list_diameters_number, list_diameters_min, 'b-')
    plt.plot(list_diameters_number, list_diameters, 'g-')
    plt.ylabel("Diameter")
    plt.xlabel("Removed nodes")
    plt.legend(['Max', 'Min', 'Average'], loc='upper right')
    plt.savefig('data/' + 'diagram_degree' + '.png', dpi=500)
    plt.show()

    # Plot of closeness diameters
    plt.plot(list_diameters_number2, list_diameters_max2, 'r-')
    plt.plot(list_diameters_number2, list_diameters_min2, 'b-')
    plt.plot(list_diameters_number2, list_diameters2, 'g-')
    plt.ylabel("Diameter")
    plt.xlabel("Removed nodes")
    plt.legend(['Max', 'Min', 'Average'], loc='upper right')
    plt.savefig('data/' + 'diagram_closeness' + '.png', dpi=500)
    plt.show()

    # Plot of betweenness diameters
    plt.plot(list_diameters_number3, list_diameters_max3, 'r-')
    plt.plot(list_diameters_number3, list_diameters_min3, 'b-')
    plt.plot(list_diameters_number3, list_diameters3, 'g-')
    plt.ylabel("Diameter")
    plt.xlabel("Removed nodes")
    plt.legend(['Max', 'Min', 'Average'], loc='upper right')
    plt.savefig('data/' + 'diagram_betweenness' + '.png', dpi=500)
    plt.show()


def prova():
    create_graph()
    g.to_undirected()
    comps = list(nx.connected_component_subgraphs(g))
    giant_comp = max(comps, key=len)  # This is a subgraph that we have to study
    print('\tGiant component:')
    print('\t\tNumber of nodes:', giant_comp.number_of_nodes())
    print(type(giant_comp.number_of_nodes()))

    print(giant_comp)
    print(type(giant_comp))


def main():
    # scale_free_robustness()
    bitcoin_robustness3()


if __name__ == '__main__':
    main()