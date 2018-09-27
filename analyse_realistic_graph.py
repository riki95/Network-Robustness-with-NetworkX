import networkx as nx
import matplotlib.pyplot as plt
import collections

file = None  # open('out', 'w')
plotOn = False
g = nx.DiGraph()


def create_graph():
    with open('bitcoin.csv') as f:
        for row in f:
            s = row.split(',')
            g.add_edge(s[0], s[1], weight=int(s[2]))


def compute_trust(g):
    trust = [0]*7605  # This because our indexes are until the number 7604

    with open('bitcoin.csv') as f:
        for row in f:
            s = row.split(',')
            trust[int(s[1])] = trust[int(s[1])] + int(s[2])

    count = 0
    for x in trust:
        if x == 0:
            count += 1
            continue
        print(count, x)
        count += 1

    if plotOn:
        # in_degree = dict(g.in_degree(weight='weight'))
        out_degree = dict(g.out_degree(weight='weight'))
        import operator
        sorted_d = sorted(out_degree.items(), key=operator.itemgetter(1), reverse=True)  # Change to indegree if we want indegree
        print(sorted_d)
        trust_list = []
        for k, v in sorted_d:
            trust_list.append(v)
        plot_distribution(trust_list, 'Out-Degree')  # Change to indegree if we want indegree


def draw_graph():
    nx.draw_networkx(g, node_size=50, font_size=2, arrowsize=3, node_color='b')
    plt.show()


# Centrality can be calculated by Degrees, Closeness or Betweenness.
def compute_centrality(g):
    nodes_degrees = nx.degree_centrality(g)
    # nodes_degrees = nx.closeness_centrality(g)
    # nodes_degrees = nx.betweenness_centrality(g)

    max_centrality = max(nodes_degrees, key=nodes_degrees.get)
    print('\n\tNode with Max number of Edges: ', max_centrality,
          ' || Degree: ', nodes_degrees[max_centrality], file=file)

    return max_centrality


def print_node_degrees(node, g):
    print('\tDegrees data for node ', node, file=file)
    print('\t\tMost important node In-Degree:', g.in_degree(node),
          ' || Weighted: ', g.in_degree(node, weight='weight'), file=file)
    print('\t\tMost important node Out-Degree:', g.out_degree(node),
          ' || Weighted: ', g.out_degree(node, weight='weight'), file=file)
    print('\t\tMost important node Total-Degree:', g.degree(node),
          ' || Weighted: ', g.degree(node, weight='weight'), file=file)


def plot_distribution(values, label):
    values_count = collections.Counter(values)
    val, cnt = zip(*values_count.items())

    fig, ax = plt.subplots()
    plt.bar(val, cnt, width=0.80, color='b')

    plt.title(label + " Histogram")
    plt.ylabel("Count")
    plt.xlabel(label)
    ax.set_xticks([v + 0.4 for v in val])
    ax.set_xticklabels(val)
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.show()


def compute_component(comps):
    print('\t\tNumber of components:', len(comps), file=file)

    diameters = [nx.diameter(comp.to_undirected()) for comp in comps]
    print('\t\tDiameter max:', max(diameters), file=file)
    print('\t\tDiameter min:', min(diameters), file=file)
    print('\t\tDiameter avg:', sum(diameters) / len(diameters), file=file)
    if plotOn:
        plot_distribution(diameters, 'diameter')

    giant_comp = max(comps, key=len)  # This is a subgraph that we have to study
    compute_centrality(giant_comp)
    print('\tGiant component:', file=file)
    print('\t\tNumber of nodes:', giant_comp.number_of_nodes(), file=file)
    print('\t\tNumber of edges:', giant_comp.number_of_edges(), file=file)

    indegree = dict(giant_comp.in_degree())
    outdegree = dict(giant_comp.out_degree())
    degree = dict(giant_comp.degree())
    if plotOn:
        plot_distribution(indegree.values(), 'indegree component')
        plot_distribution(outdegree.values(), 'outdegree component')
        plot_distribution(degree.values(), 'degree')

    print('\t\tMost important node is: \n\t\t\tIn-Degree ', max(indegree), ' || Out-Degree: ', max(outdegree),
          ' || Total Degree: ', max(degree), file=file)

    print("\t\tDensity:", nx.density(giant_comp), file=file)
    print('\t\tAverage clustering', nx.average_clustering(nx.Graph(giant_comp)), file=file)

    return giant_comp


def do_computations(g):
    print('\tNumber of nodes:', g.number_of_nodes(), file=file)
    print('\tNumber of edges:', g.number_of_edges(), file=file)
    print('\tNumber of self-loops:', g.number_of_selfloops(), file=file)

    max_centrality = compute_centrality(g)  # Need to set how to calculate centrality inside the function
    print_node_degrees(max_centrality, g)

    print('\n\tNumber of triangles:', sum(nx.triangles(g.to_undirected()).values()) / 3, file=file)
    print('\tAverage clustering:', nx.average_clustering(g.to_undirected()), file=file)

    print('\n\tStrongly connected components:', file=file)
    connected_comps_strong = list(nx.strongly_connected_component_subgraphs(g))
    strong_giant = compute_component(connected_comps_strong)
    print('\tAverage shortest path length', nx.average_shortest_path_length(strong_giant), file=file)

    print('\n\tWeakly connected components:', file=file)
    connected_comps_weak = list(nx.weakly_connected_component_subgraphs(g))
    weak_giant = compute_component(connected_comps_weak)