"""Coursework genetic algorithms; see README.md for provenance and limitations."""
import numpy as np
import random
import math


class EightQueensState:
    """This class represents a board in the eight queens puzzle"""
    def __init__(self, state=None, n=8):
        """
        :param state: pass in a numpy array of integers to set the state, otherwise will be generated randomly
        :param n: only used if state is not provided, determines size of board (default: 8)
        """
        if state is None:
            self.n = n
            state = np.random.randint(0, n, n)
        else:
            self.n = len(state)
        self.state = state

    @staticmethod
    def copy_replace(state, i, x):
        """This creates a copy of the state (important as numpy arrays are mutable) with column i set to x"""
        new_state = state.copy()
        new_state[i] = x
        return new_state

    @staticmethod
    def range_missing(start, stop, missing):
        """
        This creates a list of numbers with a single value missing
        e.g. range_missing(0, 8, 2) -> [0, 1, 3, 4, 5, 6, 7]
        """
        return list(range(start, missing)) + list(range(missing + 1, stop))

    def cost(self):
        """Calculates the number of pairs attacking"""
        count = 0
        for i in range(len(self.state) - 1):
            # for each queen, look in columns to the right
            # add one to the count if there is another queen in the same row
            count += (self.state[i] == np.array(self.state[i + 1:])).sum()

            # add one to the count for each queen on the upper or lower diagonal
            upper_diagonal = self.state[i] + np.arange(1, self.n - i)
            lower_diagonal = self.state[i] - np.arange(1, self.n - i)
            count += (np.array(self.state[i + 1:]) == upper_diagonal).sum()
            count += (np.array(self.state[i + 1:]) == lower_diagonal).sum()
        return count
    
    def neighbourhood(self):
        """This generates every state possible by changing a single queen position"""
        neighbourhood = []
        for column in range(self.n):
            for new_position in self.range_missing(0, self.n, self.state[column]):
                new_state = self.copy_replace(self.state, column, new_position)
                neighbourhood.append(EightQueensState(new_state))

        return neighbourhood

    def random_neighbour(self):
        """Generates a single random neighbour state, useful for some algorithms"""
        column = np.random.choice(range(self.n))
        new_position = np.random.choice(self.range_missing(0, self.n, self.state[column]))
        new_state = self.copy_replace(self.state, column, new_position)
        return EightQueensState(new_state)

    def is_goal(self):
        return self.cost() == 0

    def __str__(self):
        if self.is_goal():
            return f"Goal state! {self.state}"
        else:
            return f"{self.state} cost {self.cost()}"

class GeneticAlgorithm:
    def __init__(self, pop_size=30, min_mutation_rate=0.05, max_mutation_rate = 0.3, boost_threshold = 3, extinction_threshold = 15, 
                 boost_multiple = 0.6, max_gen=5000, tournament_size=5):
        self.pop_size = pop_size
        self.mutation_rate = max_mutation_rate
        self.max_gen = max_gen
        self.tournament_size = tournament_size
        self.min_mutation_rate = min_mutation_rate
        self.max_mutation_rate = max_mutation_rate
        self.boost_threshold = boost_threshold
        self.boost_multiple = boost_multiple
        self.extinction_threshold = extinction_threshold

    def initialise_population(self):
        
        # I tried to edit the initialise_population method to include survivors (the elites) from the previous generation, but the dominance of the survivors actually led the algorithm to remain in its local optimum trap, so I kept the original method.
        # this unused edit is left here commented out.
        # if survivors:
        #     return survivors + [EightQueensState() for _ in range(self.pop_size - len(survivors))]
        # else:
            
            return [EightQueensState() for _ in range(self.pop_size)]

    def fitness(self, state):
        # Other approaches use fitness functions that count the number of non-attacking pairs. 
        # This approach can be effectively replicated by subtracting the cost from 8c2 = 28,
        # which is the maximum number of non-attacking pairs in the 8-queens problem.
        # See:
        # https://www.educative.io/answers/solving-the-8-queen-problem-using-genetic-algorithm
        # https://medium.com/nerd-for-tech/genetic-algorithm-8-queens-problem-b01730e673fd
        return 28 - state.cost()

    def tournament(self, population):
        # Roulette approach and tournament approach were tried, but tournament approach proved to be better.
        # Both were suggested in literature.
        tournament = random.sample(population, self.tournament_size)
        best = min(tournament, key=lambda i: i.cost())
        return best

    def selection(self, population):
        # Select two parents using tournament selection
        parent1 = self.tournament(population)
        parent2 = self.tournament(population)
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # Single point crossover
        crossover_point = random.randint(0, parent1.n - 1)
        child_state = np.concatenate((parent1.state[:crossover_point], parent2.state[crossover_point:]))
        return EightQueensState(state=child_state)

    def mutate(self, child):
        # Randomly mutate a column with some probability
        if random.random() < self.mutation_rate:
            column = random.randint(0, child.n - 1)
            new_position = random.randint(0, child.n - 1)
            child.state = EightQueensState.copy_replace(child.state, column, new_position)
        return child

    def run(self):
        population = self.initialise_population()
        elite_count = max(1, int(0.05 * self.pop_size))  # Top 5% for elitism
        best_cost = min(population, key=lambda state: state.cost()).cost()
        stagnation_counter = 0
        
        record = []
        mutation_param = 0  # Used to adjust mutation rate dynamically
        for generation in range(self.max_gen):
            # Adjust mutation rate dynamically (higher initially, lower as generations progress)
            self.mutation_rate = max(self.min_mutation_rate, self.max_mutation_rate * (1 - mutation_param / self.max_gen))
            mutation_param += 1
            
            # Sort population by fitness (cost), ascending, and select elites
            population.sort(key=lambda individual: individual.cost())
            elites = population[:elite_count]

            # track the best cost in each generation for later analysis
            record.append(elites[0].cost())
            
            # Check if the best individual is a solution
            if elites[0].is_goal():
                print(f"Solution found in generation {generation}: {elites[0]}")
                return elites[0], record
            
            # Check for improvement and apply feedback loop to mutation rate if needed
            current_best_cost = elites[0].cost()
            if current_best_cost < best_cost:
                best_cost = current_best_cost
                stagnation_counter = 0  # Reset stagnation counter if there's improvement
            else:
                stagnation_counter += 1
            
            # If stagnation occurs, increase mutation rate temporarily
            if stagnation_counter >= self.boost_threshold:
                self.mutation_rate = self.mutation_rate * (1 + self.boost_multiple)  # Increase mutation rate by 50%
            
            # If stagnation reaches the extinction threshold, reset the population
            if stagnation_counter >= self.extinction_threshold:
                print(f"Extinction event in generation {generation}")
                population = self.initialise_population()  # Extinction event
                best_cost = min(population, key=lambda state: state.cost()).cost()
                stagnation_counter = 0
                mutation_param = 0
            else:
                # Create the next generation with elites preserved
                new_population = elites.copy()
                while len(new_population) < self.pop_size:
                    parent1, parent2 = self.selection(population)
                    child = self.crossover(parent1, parent2)
                    child = self.mutate(child)
                    new_population.append(child)
                
                population = new_population  # Replace old population with new one
        
        # If no solution found, return best guess
        best_guess = min(population, key=lambda state: state.cost())
        print(f"No exact solution found. Best guess: {best_guess}")
        return best_guess, record

class ToroidalQueensState:
    """This class represents a board in the eight queens puzzle"""
    def __init__(self, state=None, n=7):
        """
        :param state: pass in a numpy array of integers to set the state, otherwise will be generated randomly
        :param n: only used if state is not provided, determines size of board (default: 8)
        """
        if state is None:
            self.n = n
            state = np.random.randint(0, n, n)
        else:
            self.n = len(state)
        self.state = state

    @staticmethod
    def copy_replace(state, i, x):
        """This creates a copy of the state (important as numpy arrays are mutable) with column i set to x"""
        new_state = state.copy()
        new_state[i] = x
        return new_state

    @staticmethod
    def range_missing(start, stop, missing):
        """
        This creates a list of numbers with a single value missing
        e.g. range_missing(0, 8, 2) -> [0, 1, 3, 4, 5, 6, 7]
        """
        return list(range(start, missing)) + list(range(missing + 1, stop))

    def cost(self):
        """
        Calculates the number of attacking queen pairs on a toroidal board by considering each pair of queens and whether they are attacking.
        """
        count = 0
        # The double-for loop is used to consider all the queens as pairs. Since the board now wraps around, the previous approach
        # of just considering queens "to the right" of the current queen is no longer valid, although this adds to the computational complexity.
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                # I calculate the difference in the number of rows between two queens. Since the board wraps around,
                # The distance between two queens that are far away on a traditional board can become close together once that
                # board is wrapped aroung into a toroidal board, so I take the minimum of the distances both from a traditional
                # board setup and the distance considering the position from the other side of the board. This latter distance
                # can be obtained by subtracting the traditional distance from the board size, since the sum of the difference between two
                # pieces on a traditional setup and the difference "from the other side" must equal the board size.
                trad_diff = abs(self.state[i] - self.state[j])
                toro_diff = self.n - trad_diff
                row_diff = min(trad_diff, toro_diff)
                
                # I do the same for the column difference
                trad_diff = abs(i - j)
                toro_diff = self.n - trad_diff
                col_diff = min(trad_diff, toro_diff)
                
                # Attacks can happen if the queens are in the same row or on a diagonal (since they are in different columns by design).
                # This is the case if:
                # - row_diff == 0
                # - row_diff == col_diff
                if row_diff == 0 or row_diff == col_diff:
                    count += 1  # Increase count for each pair of attacking queens

        return count
    
    def neighbourhood(self):
        """This generates every state possible by changing a single queen position"""
        neighbourhood = []
        for column in range(self.n):
            for new_position in self.range_missing(0, self.n, self.state[column]):
                new_state = self.copy_replace(self.state, column, new_position)
                neighbourhood.append(ToroidalQueensState(new_state))

        return neighbourhood

    def random_neighbour(self):
        """Generates a single random neighbour state, useful for some algorithms"""
        column = np.random.choice(range(self.n))
        new_position = np.random.choice(self.range_missing(0, self.n, self.state[column]))
        new_state = self.copy_replace(self.state, column, new_position)
        return ToroidalQueensState(new_state)

    def is_goal(self):
        return self.cost() == 0

    def __str__(self):
        if self.is_goal():
            return f"Goal state! {self.state}"
        else:
            return f"{self.state} cost {self.cost()}"

class ToroidalGeneticAlgorithm:
    def __init__(self, n = 7, pop_size=30, min_mutation_rate=0.05, max_mutation_rate = 0.3, boost_threshold = 3, extinction_threshold = 50, 
                 boost_multiple = 0.6, max_gen=5000, tournament_size=5):
        self.pop_size = pop_size
        self.mutation_rate = max_mutation_rate
        self.max_gen = max_gen
        self.tournament_size = tournament_size
        self.min_mutation_rate = min_mutation_rate
        self.max_mutation_rate = max_mutation_rate
        self.boost_threshold = boost_threshold
        self.boost_multiple = boost_multiple
        self.extinction_threshold = extinction_threshold
        self.n = n

    def initialise_population(self):
        
            # The initialisation method is modified to allow for different board sizes.

            return [ToroidalQueensState(n=self.n) for _ in range(self.pop_size)]

    def fitness(self, state):
        # The fitness method is also altered to account for any board size by calculating the maximum number of non-attacking pairs (board size choose 2) and subtracting the cost.
        return math.comb(self.n, 2) - state.cost()

    def tournament(self, population):
        # Roulette approach and tournament approach were tried, but tournament approach proved to be better.
        # Both were suggested in literature.
        tournament = random.sample(population, self.tournament_size)
        best = min(tournament, key=lambda i: i.cost())
        return best

    def selection(self, population):
        # Select two parents using tournament selection
        parent1 = self.tournament(population)
        parent2 = self.tournament(population)
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # Single point crossover
        crossover_point = random.randint(0, parent1.n - 1)
        child_state = np.concatenate((parent1.state[:crossover_point], parent2.state[crossover_point:]))
        return ToroidalQueensState(state=child_state)

    def mutate(self, child):
        # Randomly mutate a column with some probability
        if random.random() < self.mutation_rate:
            column = random.randint(0, child.n - 1)
            new_position = random.randint(0, child.n - 1)
            child.state = ToroidalQueensState.copy_replace(child.state, column, new_position)
        return child

    def run(self):
        population = self.initialise_population()
        elite_count = max(1, int(0.05 * self.pop_size))  # Top 5% for elitism
        best_cost = min(population, key=lambda state: state.cost()).cost()
        stagnation_counter = 0
        
        record = []
        mutation_param = 0  # Used to adjust mutation rate dynamically
        for generation in range(self.max_gen):
            # Adjust mutation rate dynamically (higher initially, lower as generations progress)
            self.mutation_rate = max(self.min_mutation_rate, self.max_mutation_rate * (1 - mutation_param / self.max_gen))
            mutation_param += 1
            
            # Sort population by fitness (cost), ascending, and select elites
            population.sort(key=lambda individual: individual.cost())
            elites = population[:elite_count]

            # track the best cost in each generation for later analysis
            record.append(elites[0].cost())
            
            # Check if the best individual is a solution
            if elites[0].is_goal():
                print(f"Solution found in generation {generation}: {elites[0]}")
                return elites[0], record
            
            # Check for improvement and apply feedback loop to mutation rate if needed
            current_best_cost = elites[0].cost()
            if current_best_cost < best_cost:
                best_cost = current_best_cost
                stagnation_counter = 0  # Reset stagnation counter if there's improvement
            else:
                stagnation_counter += 1
            
            # If stagnation occurs, increase mutation rate temporarily
            if stagnation_counter >= self.boost_threshold:
                self.mutation_rate = self.mutation_rate * (1 + self.boost_multiple)  # Increase mutation rate by 50%
            
            # If stagnation reaches the extinction threshold, reset the population
            if stagnation_counter >= self.extinction_threshold:
                print(f"Extinction event in generation {generation}")
                population = self.initialise_population()  # Extinction event
                best_cost = min(population, key=lambda state: state.cost()).cost()
                stagnation_counter = 0
                mutation_param = 0
            else:
                # Create the next generation with elites preserved
                new_population = elites.copy()
                while len(new_population) < self.pop_size:
                    parent1, parent2 = self.selection(population)
                    child = self.crossover(parent1, parent2)
                    child = self.mutate(child)
                    new_population.append(child)
                
                population = new_population  # Replace old population with new one
        
        # If no solution found, return best guess
        best_guess = min(population, key=lambda state: state.cost())
        print(f"No exact solution found. Best guess: {best_guess}")
        return best_guess, record
