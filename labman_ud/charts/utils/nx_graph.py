# -*- encoding: utf-8 -*-

from charts.utils import community

import networkx as nx


def analyze(G):
    components = []

    components = nx.connected_component_subgraphs(G)

    i = 0

    for cc in components:
        #Set the connected component for each group
        for node in cc:
            G.node[node]['component'] = i

        #Calculate the in component betweeness, closeness and eigenvector centralities
        cent_betweenness = nx.betweenness_centrality(cc)
        # cent_eigenvector = nx.eigenvector_centrality_numpy(cc)
        cent_eigenvector = nx.eigenvector_centrality(cc)
        cent_closeness = nx.closeness_centrality(cc)

        for name in cc.nodes():
            G.node[name]['cc-betweenness'] = cent_betweenness[name]
            G.node[name]['cc-eigenvector'] = cent_eigenvector[name]
            G.node[name]['cc-closeness'] = cent_closeness[name]

        i += 1

    # Calculate cliques
    cliques = list(nx.find_cliques(G))
    j = 0
    processed_members = []
    for clique in cliques:
        for member in clique:
            if not member in processed_members:
                G.node[member]['cliques'] = []
                processed_members.append(member)
            G.node[member]['cliques'].append(j)
        j += 1

    #calculate degree
    degrees = G.degree()
    for name in degrees:
        G.node[name]['degree'] = degrees[name]

    betweenness = nx.betweenness_centrality(G)
    eigenvector = nx.eigenvector_centrality_numpy(G)
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)
    k_cliques = nx.k_clique_communities(G, 3)

    for name in G.nodes():
        G.node[name]['betweenness'] = betweenness[name]
        G.node[name]['eigenvector'] = eigenvector[name]
        G.node[name]['closeness'] = closeness[name]
        G.node[name]['pagerank'] = pagerank[name]

    for pos, k_clique in enumerate(k_cliques):
        for member in k_clique:
            G.node[member]['k-clique'] = pos

    partitions = community.best_partition(G)

    for key in partitions.keys():
        G.node[key]['modularity'] = partitions[key]

    return G
