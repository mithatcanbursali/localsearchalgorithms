# author: Mithatcan Bursalı
import random
import copy


def random_problem_generator(n):
    problems = []
    for _ in range(10):
        problems.append([[random.randint(1, 4) for _ in range(n)] for _ in range(n)])
    return problems


def fitness_calculator(problem):
    fitness = 0
    n = len(problem)

    for j in range(n):
        for k in range(n):
            if k < n - 1 and problem[j][k] == problem[j][k + 1]:
                fitness += 1
            if j < n - 1 and problem[j][k] == problem[j + 1][k]:
                fitness += 1
    return fitness


def get_neighbors(current_position):
    neighbors = []
    n = len(current_position)
    for i in range(n):
        for j in range(n):
            for color in range(1, 5):
                if current_position[i][j] != color:
                    neighbor = copy.deepcopy(current_position)
                    neighbor[i][j] = color
                    neighbors.append(neighbor)

    return neighbors


def create_population(inital_state, population_number):
    n = len(inital_state)
    population = []
    for _ in range(population_number):
        population_member = copy.deepcopy(inital_state)
        population_member[random.randint(0, n - 1)][random.randint(0, n - 1)] = random.randint(1, 4)
        population.append(population_member)
    return population


def mutation(n):
    return [[random.randint(1, 4) for _ in range(n)] for _ in range(n)]


def crossover(population):
    n = len(population)
    best_generation_number = int(0.1 * n)
    next_generation = []
    next_generation.extend(population[:best_generation_number])

    while len(next_generation) < len(population):
        parent_1 = random.choice(population[:best_generation_number])
        parent_2 = random.choice(population[:best_generation_number])
        child = copy.deepcopy(parent_1)

        for i in range (len(child)):
            for k in range(len(child)):
                prob = random.random()

                if prob < 0.45:
                    child[i][k] = parent_1[i][k]
                elif prob < 0.9:
                    child[i][k] = parent_2[i][k]
                else:  # Mutation rate set to %10 by default
                    child[i][k] = mutation(n)[i][k]
        next_generation.append(child)

    return next_generation


def genetic_algorithm(inital_state, population_number):
    population = create_population(inital_state, population_number)
    generations = 1
    flag = 0
    solution_index = 0
    while flag == 0:
        population_fitnesses = []
        for population_fitness in population:
            population_fitnesses.append(fitness_calculator(population_fitness))

        population = [population for (population_fitnesses, population) in sorted(zip(population_fitnesses, population), key=lambda pair: pair[0])]

        if fitness_calculator(population[0]) != 0:
            print(f"Generation:{generations}, best fitness: {fitness_calculator(population[0])}")
            generations +=1

        if 0 in population_fitnesses:
            population_fitnesses.sort()
            solution_index = population_fitnesses.index(0)
            flag = 1
        else:
            population = crossover(population)

    return population[solution_index],generations


def hill_climbing_search(initial_state):
    current_position = initial_state
    default_iteration = 1000 # Maximum Iteration set to 1000 default
    for _ in range(default_iteration):
        current_cost = fitness_calculator(current_position)
        neighbors = get_neighbors(current_position)
        neighbor_fitnesses = []
        for neighbor in neighbors:
            neighbor_fitnesses.append(fitness_calculator(neighbor))

        best_neighbor = neighbors[neighbor_fitnesses.index(min(neighbor_fitnesses))]
        if current_cost >= min(neighbor_fitnesses):
            current_position = best_neighbor
    return current_position, current_cost


# Driver Code
if __name__ == "__main__":
    # 1 represents blue, 2 represents aqua, 3 represents red, 4 represents orange
    n = int(input("Which size you want to create(for 10x10, type 10):"))
    problems = random_problem_generator(n)
    for i in range(10):

        current_position = problems[i]
        print(f"Problem {i + 1}:")
        for row in current_position:
            print(f"{row}")
        print("\n")
        print("Hill Climbing Algorithm:")
        hill_climb_solution = hill_climbing_search(current_position)
        print("Solution:")
        for row in hill_climb_solution[0]:
            print(f"{row}")
        print(f"Fitness:{hill_climb_solution[1]}\n")

        print("Genetic Algorithm:")
        genetic_solution = genetic_algorithm(current_position, 100)
        print(f"\nSolution found on Generation {genetic_solution[1]}:")
        for row in genetic_solution[0]:
            print(f"{row}")
        print("\n")

