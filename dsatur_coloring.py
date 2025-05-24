import itertools
import random
import networkx as nx

def dsatur_coloring(graph):
    coloring = {}
    saturation = {node: 0 for node in graph.nodes()}
    degrees = dict(graph.degree())
    while len(coloring) < graph.number_of_nodes():
        u = max((node for node in graph.nodes() if node not in coloring), key=lambda x: (saturation[x], degrees[x]))
        forbidden = {coloring[nbr] for nbr in graph.neighbors(u) if nbr in coloring}
        color = next(c for c in itertools.count() if c not in forbidden)
        coloring[u] = color
        for nbr in graph.neighbors(u):
            if nbr not in coloring:
                neighbor_forbidden = {coloring[n] for n in graph.neighbors(nbr) if n in coloring}
                saturation[nbr] = len(neighbor_forbidden)
    return coloring

def count_conflicts(graph, solution):
    conflicts = 0
    for u, v in graph.edges():
        if solution[u] == solution[v]:
            conflicts += 1
    return conflicts

def tabu_search_reassign(graph, solution, num_colors, max_iter=1000, tabu_tenure=7):
    current_solution = solution.copy()
    for node in graph.nodes():
        if current_solution[node] is None:
            current_solution[node] = random.randint(0, num_colors - 1)
    best_solution = current_solution.copy()
    best_conflicts = count_conflicts(graph, current_solution)
    tabu_list = {}
    iteration = 0
    while iteration < max_iter and best_conflicts > 0:
        current_conflicts = count_conflicts(graph, current_solution)
        best_move = None
        best_move_delta = float('inf')
        for node in graph.nodes():
            for new_color in range(num_colors):
                if current_solution[node] == new_color:
                    continue
                old_color = current_solution[node]
                delta = 0
                for neighbor in graph.neighbors(node):
                    if current_solution[neighbor] == old_color:
                        delta -= 1
                    if current_solution[neighbor] == new_color:
                        delta += 1
                if (node, new_color) in tabu_list and tabu_list[(node, new_color)] > iteration:
                    if current_conflicts + delta >= best_conflicts:
                        continue
                if delta < best_move_delta:
                    best_move_delta = delta
                    best_move = (node, new_color)
        if best_move is None:
            break
        node, new_color = best_move
        old_color = current_solution[node]
        current_solution[node] = new_color
        tabu_list[(node, old_color)] = iteration + tabu_tenure
        new_conflicts = count_conflicts(graph, current_solution)
        if new_conflicts < best_conflicts:
            best_conflicts = new_conflicts
            best_solution = current_solution.copy()
        iteration += 1
    success = (best_conflicts == 0)
    return best_solution, success

def tabu_search_reduce_colors(graph, initial_solution, max_iter=1000, tabu_tenure=7):
    current_solution = initial_solution.copy()
    k = max(initial_solution.values()) + 1
    best_solution = current_solution.copy()
    while k > 1:
        new_solution = current_solution.copy()
        nodes_to_reassign = [node for node, col in new_solution.items() if col == k - 1]
        for node in nodes_to_reassign:
            new_solution[node] = None
        candidate_solution, success = tabu_search_reassign(graph, new_solution, k - 1, max_iter, tabu_tenure)
        if success:
            current_solution = candidate_solution
            best_solution = candidate_solution
            k -= 1
        else:
            break
    return best_solution

def dsatur_tabu_coloring(graph, max_iter=1000, tabu_tenure=7):
    initial = dsatur_coloring(graph)
    improved = tabu_search_reduce_colors(graph, initial, max_iter, tabu_tenure)
    return improved

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                         ALGORYTM DSATUR + TABU SEARCH                    ║
# ║                       Parametry strojenia heurystyki                     ║
# ║                         © Kubiak & Żurczak · 2025                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# max_iter           → Maksymalna liczba iteracji tabu search.
#                      Większa = dokładniejsze przeszukiwanie, ale wolniejsze działanie.
#                      Wartość typowa: 500–5000, zależnie od rozmiaru grafu.

# tabu_tenure        → Długość zakazu cofania zmian (długość listy tabu).
#                      Wyższa wartość = większa różnorodność, ale wolniejsza zbieżność.
#                      Typowo 5–15 lub dynamiczna np. sqrt(n).

# current_solution[node] = randint(...)
#                    → Metoda inicjalizacji kolorów wierzchołków do ponownego pokolorowania.
#                      Lepsze: przypisz kolor najmniej używany w sąsiedztwie lub o najmniejszym konflikcie.

# delta              → Zmiana liczby konfliktów dla danego ruchu.
#                      Używane do wyboru najlepszego ruchu w danej iteracji (ruch o najmniejszym delta).

# success            → Flaga określająca, czy udało się uzyskać kolorowanie bez konfliktów
#                      po redukcji liczby kolorów.

# nodes_to_reassign  → Lista wierzchołków do rekonstrukcji po usunięciu najwyższego koloru.
#                      Ich ponowne przypisanie decyduje o sukcesie redukcji liczby kolorów.
