import networkx as nx
from greedy_coloring import greedy_coloring
from dsatur_coloring import dsatur_coloring

def load_graph_from_stream(stream):
    lines = stream.read().decode().splitlines()
    n = int(lines[0].strip())
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for line in lines[1:]:
        u, v = map(int, line.split())
        G.add_edge(u, v)
    return G

def compute_colorings(graph):
    greedy = greedy_coloring(graph)
    dsatur = dsatur_coloring(graph)
    return {
        'Greedy': {
            'valid': all(greedy[u] != greedy[v] for u, v in graph.edges()),
            'colors': len(set(greedy.values()))
        },
        'DSatur': {
            'valid': all(dsatur[u] != dsatur[v] for u, v in graph.edges()),
            'colors': len(set(dsatur.values()))
        }
    }

if __name__ == '__main__':
    import sys
    fname = sys.argv[1] if len(sys.argv) > 1 else 'graph.txt'
    with open(fname, 'rb') as f:
        G = load_graph_from_stream(f)
    results = compute_colorings(G)
    for name,data in results.items():
        print(f"{name} — Valid: {data['valid']} | Colors: {data['colors']}")