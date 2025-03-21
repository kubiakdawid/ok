import random
#Define the objective function to be minimized
def objective_function(x):
    return x ** 2

# Initialize the current solution and best solution
current_solution = random.randint(-10, 10)
best_solution = current_solution
# Define the tabu list and its length
tabu_list = []
tabu_list_length = 5
# Set the maximum number of iterations
max_iterations = 100
# Begin the search
for i in range(max_iterations):
    # Generate a list of possible moves
    moves = [-1, 1]
    # Define the best move and its corresponding value
    best_move = None
    best_value = float('inf')
    # Evaluate the value of each move
    for move in moves:
        candidate = current_solution + move
        if candidate not in tabu_list:
            candidate_value = objective_function(candidate)
            if candidate_value < best_value:
                best_move = move
                best_value = candidate_value
    # Update the current solution and tabu list
    current_solution += best_move
    tabu_list.append(current_solution)
    # If the tabu list becomes too long, remove the oldest element
    if len(tabu_list) > tabu_list_length:
        tabu_list.pop(0)
    # Update the best solution if necessary
    if objective_function(current_solution) < objective_function(best_solution):
        best_solution = current_solution
# Print the final solution
print("Best solution: ", best_solution)