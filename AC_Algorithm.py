import numpy as np


def ant_colony_coloring(graph, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1):
    n_nodes = graph.number_of_nodes()
    pheromone = np.ones((n_nodes, n_nodes))
    best_coloring = None
    best_color_count = float('inf')

    for _ in range(n_iterations):
        paths = []
        color_counts = []

        for _ in range(n_ants):
            coloring = {}
            available_colors = set()
            nodes = list(graph.nodes())
            np.random.shuffle(nodes)

            for node in nodes:
                adjacent_colors = {coloring.get(neighbour) for neighbour in graph.neighbors(node) if
                                   neighbour in coloring}
                probabilities = np.zeros(len(available_colors) + 1)

                for i, color in enumerate(available_colors):
                    probabilities[i] = pheromone[node, i] ** alpha / (1 + len(adjacent_colors & {color})) ** beta
                probabilities[-1] = 1  # New color option

                probabilities /= np.sum(probabilities)
                chosen_color = np.random.choice(len(probabilities), p=probabilities)

                if chosen_color == len(available_colors):
                    chosen_color = len(available_colors)
                    available_colors.add(chosen_color)

                coloring[node] = chosen_color

            color_count = len(set(coloring.values()))
            paths.append(coloring)
            color_counts.append(color_count)

            if color_count < best_color_count:
                best_coloring = coloring
                best_color_count = color_count

        pheromone *= evaporation_rate

        for path, color_count in zip(paths, color_counts):
            for node, color in path.items():
                pheromone[node, color] += Q / color_count

    return best_coloring