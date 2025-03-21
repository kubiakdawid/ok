import itertools

def greedy_coloring(graph):
    coloring = {}
    for node in graph.nodes():
        forbidden = {coloring.get(neighbour) for neighbour in graph.neighbors(node)}
        coloring[node] = next(color for color in itertools.count() if color not in forbidden)
    return coloring
