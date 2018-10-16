import matplotlib.pyplot as plt
import networkx as nx
import heapq


from Lab1.analyse_realistic_graph import do_computations, create_graph, compute_centrality, plot_distribution

g = nx.Graph().to_undirected()
node_pose = {}
drawGraphOn = True
plotOn = True
diametersOn = True
plotDiametersOn = True


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


# when you do this remember do compute degree on analysis
def bitcoin_robustness():
    create_graph()
    g.to_undirected()
    pos = nx.spring_layout(g)

    #do_computations(g, 'g_start', 'degree')

    g_remove_most_important = g.copy()
    list_components = []
    list_removed = []
    list_removed2 = [0, 100,200,300,400,500,600,700,800,900,1000]
    list_diameters = []
    list_diameters_number = []
    list_diameters_max = []
    list_diameters_min = []
    list_giantcomponentnodes = []

    if drawGraphOn:
        draw_graph(g, pos, "Graph", 'g1')

    print("::: Computing Degree :::")
    for x in range(1001):
        best_node, nodes = compute_centrality(g_remove_most_important, 'degree')

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()
        comp_len = len(comps)

        if x == 0 or x == 100 or x == 200 or x == 300 or x == 400 or x == 500 or x == 600 or x == 700 or x == 800 \
                or x == 900 or x == 1000:
            print('----- Nodes removed: ', x, ' -----')
            if diametersOn:
                diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
                list_diameters_max.append(max(diameters))
                list_diameters_min.append(min(diameters))
                list_diameters.append(sum(diameters) / len(diameters))
                list_diameters_number.append(x)

                if plotDiametersOn and x == 1000:
                    degree = dict(giant_comp.degree())
                    plot_distribution(degree.values(), 'degree')

            list_giantcomponentnodes.append(comp_nodes_number)

        list_components.append(comp_len)
        list_removed.append(x)

        g_remove_most_important.remove_nodes_from([best_node])

    if drawGraphOn:
        do_computations(g_remove_most_important, 'degree', 'degree')
        draw_graph(g_remove_most_important, pos, "Graph with removal by degree", 'g2_degree')
        plt.show()

    g_remove_most_important = g.copy()
    list_components2 = []
    list_giantcomponentnodes2 = []
    list_diameters2 = []
    list_diameters_number2 = []
    list_diameters_max2 = []
    list_diameters_min2 = []

    print("::: Computing Closeness :::")
    for x in range(11):
        print('----- Nodes removed: ', x, ' -----')
        best_node, nodes = compute_centrality(g_remove_most_important, 'closeness')
        first_nodes = heapq.nlargest(100, nodes, key=nodes.get)

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        comp_len = len(comps)
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()

        if diametersOn:
            diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
            list_diameters_max2.append(max(diameters))
            list_diameters_min2.append(min(diameters))
            list_diameters2.append(sum(diameters) / len(diameters))
            list_diameters_number2.append(x)

            if plotDiametersOn and x == 10:
                degree = dict(giant_comp.degree())
                plot_distribution(degree.values(), 'degree')

        list_giantcomponentnodes2.append(comp_nodes_number)
        list_components2.append(comp_len)

        g_remove_most_important.remove_nodes_from(first_nodes)

    if drawGraphOn:
        do_computations(g_remove_most_important, 'closeness', 'closeness')
        draw_graph(g_remove_most_important, pos, "Graph with removal by closeness", 'g3_closeness')
        plt.show()

    g_remove_most_important = g.copy()
    list_components3 = []
    list_giantcomponentnodes3 = []
    list_diameters3 = []
    list_diameters_number3 = []
    list_diameters_max3 = []
    list_diameters_min3 = []

    print("::: Computing Betweenness :::")
    for x in range(11):
        print('----- Nodes removed: ', x, ' -----')
        best_node, nodes = compute_centrality(g_remove_most_important, 'betweenness')
        first_nodes = heapq.nlargest(100, nodes, key=nodes.get)

        comps = list(nx.connected_component_subgraphs(g_remove_most_important))
        comp_len = len(comps)
        giant_comp = max(comps, key=len)
        comp_nodes_number = giant_comp.number_of_nodes()

        if diametersOn:
            diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
            list_diameters_max3.append(max(diameters))
            list_diameters_min3.append(min(diameters))
            list_diameters3.append(sum(diameters) / len(diameters))
            list_diameters_number3.append(x)

            if plotDiametersOn and x == 10:
                degree = dict(giant_comp.degree())
                plot_distribution(degree.values(), 'degree')

        list_giantcomponentnodes3.append(comp_nodes_number)
        list_components3.append(comp_len)

        g_remove_most_important.remove_nodes_from(first_nodes)

    if drawGraphOn:
        do_computations(g_remove_most_important, 'betweenness', 'betweenness')
        draw_graph(g_remove_most_important, pos, "Graph with removal by betweenness", 'g3_betweenness')
        plt.show()

    if plotOn:
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
        plt.legend(['Degree', 'Closeness', 'Betweenness'], loc='upper right')
        plt.savefig('data/' + 'giantcomponents' + '.png', dpi=500)
        plt.show()

        # Plot of degree diameters
        plt.plot(list_removed2, list_diameters_max, 'r-')
        plt.plot(list_removed2, list_diameters_min, 'b-')
        plt.plot(list_removed2, list_diameters, 'g-')
        plt.ylabel("Diameter")
        plt.xlabel("Removed nodes")
        plt.legend(['Max', 'Min', 'Average'], loc='upper right')
        plt.savefig('data/' + 'diagram_degree' + '.png', dpi=500)
        plt.show()

        # Plot of closeness diameters
        plt.plot(list_removed2, list_diameters_max2, 'r-')
        plt.plot(list_removed2, list_diameters_min2, 'b-')
        plt.plot(list_removed2, list_diameters2, 'g-')
        plt.ylabel("Diameter")
        plt.xlabel("Removed nodes")
        plt.legend(['Max', 'Min', 'Average'], loc='upper right')
        plt.savefig('data/' + 'diagram_closeness' + '.png', dpi=500)
        plt.show()

        # Plot of betweenness diameters
        plt.plot(list_removed2, list_diameters_max3, 'r-')
        plt.plot(list_removed2, list_diameters_min3, 'b-')
        plt.plot(list_removed2, list_diameters3, 'g-')
        plt.ylabel("Diameter")
        plt.xlabel("Removed nodes")
        plt.legend(['Max', 'Min', 'Average'], loc='upper right')
        plt.savefig('data/' + 'diagram_betweenness' + '.png', dpi=500)
        plt.show()

        # Plot of giant + components
        plt.plot(list_removed, list_components, 'r-')
        plt.plot(list_removed2, list_components2, 'b-')
        plt.plot(list_removed2, list_components3, 'g-')

        plt.plot(list_diameters_number, list_giantcomponentnodes, 'c-')
        plt.plot(list_removed2, list_giantcomponentnodes2, 'm-')
        plt.plot(list_removed2, list_giantcomponentnodes3, 'y-')

        plt.ylabel("Components number and Giant Component number of nodes")
        plt.xlabel("Removed nodes")
        plt.legend(['Degree', 'Closeness', 'Betweenness', 'Degree_Giant', 'Closeness_Giant', 'Betweenness_Giant'],
                   loc='upper right')
        plt.savefig('data/' + 'centralities_and_giant' + '.png', dpi=500)
        plt.show()


def main():
    # scale_free_robustness()
    # sf_robustness()
     bitcoin_robustness()


if __name__ == '__main__':
    main()