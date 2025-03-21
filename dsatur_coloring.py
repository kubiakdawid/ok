import itertools

def dsatur_coloring(graph):
    coloring = {}
    saturation = {node: 0 for node in graph.nodes()}
    degrees = dict(graph.degree())

    while len(coloring) < graph.number_of_nodes():
        u = max(
            (node for node in graph.nodes() if node not in coloring),
            key=lambda x: (saturation[x], degrees[x])
        )
        forbidden = {coloring[nbr] for nbr in graph.neighbors(u) if nbr in coloring}
        color = next(c for c in itertools.count() if c not in forbidden)
        coloring[u] = color

        for nbr in graph.neighbors(u):
            if nbr not in coloring:
                neighbor_forbidden = {coloring[n] for n in graph.neighbors(nbr) if n in coloring}
                saturation[nbr] = len(neighbor_forbidden)

    return coloring
