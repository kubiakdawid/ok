import itertools
import networkx as nx
from networkx.classes import graph
class Generator:
    def metoda_a(self):
        print("Metoda instancyjna z klasy A")

class AC_Algorithm:
    def metoda_b(self):
        obiekt_a = A()  # Tworzymy obiekt klasy A
        obiekt_a.metoda_a()  # Wywołujemy metodę z klasy A

b = B()
b.metoda_b()

def is_valid_coloring(graph, coloring):
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True


def greedy_coloring(graph):
    coloring = {}
    for node in graph.nodes():
        adjacent_colors = {coloring.get(neighbour) for neighbour in graph.neighbors(node)}
        coloring[node] = next(color for color in itertools.count() if color not in adjacent_colors)
    return coloring


def load_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

        n_nodes = int(lines[0].strip())

        G = nx.Graph()
        G.add_nodes_from(range(n_nodes))

        for line in lines[1:]:
            u, v = map(int, line.strip().split())
            G.add_edge(u, v)

        return G


filename = "graph.txt"  #Nazwa pliku
G = load_graph_from_file(filename)

coloring_result = greedy_coloring(G)

print('Coloring:', coloring_result) #Kolory wierzchołków
print('Valid:', is_valid_coloring(G, coloring_result)) #Poprawność
print('K:', len(set(coloring_result.values()))) #Ilość kolorów

ac_result = ant_colony_coloring(graph, 10, 100, 1, 1, 0.5, 1)
ac_color_count = len(set(ac_result.values()))
print(f'Ant Colony Coloring: {ac_result}')
print(f'Ant Colony K: {ac_color_count}')