## Lab 8 - Basic code for GA
## The point of this is to demonstrate how a GA can optimize a list of integers
## to sum to a particular target value.

import random, copy

class Genome(object):
  def __init__(self, genome_length):
    self.__genome  = []
    self.__fitness = 0.0
    self.__maxval  = 1000
    for i in range(genome_length):
      self.__genome.append(random.randint(0,self.__maxval))

  def Mutate(self):
    index = random.randint(0,len(self.__genome)-1)

    assert(index < len(self.__genome))
    self.__genome[index] = random.randint(0,self.__maxval)

  # Get/Set functions
  def getGenome(self):
    return self.__genome
  def setFitness(self, fitness):
    self.__fitness = fitness
  def getFitness(self):
    return self.__fitness
  def setGenome(self, genome):
    self.__genome = copy.deepcopy(genome)

class GA(object):
  def __init__(self, num_generations,
                     population_size,
                     crossover_rate,
                     mutation_rate,
                     target, 
                     genome_length):

    self.__target          = target
    self.__num_generations = num_generations
    self.__population_size = population_size
    self.__genome_length   = genome_length

    self.__crossover_rate  = crossover_rate
    self.__mutation_rate   = mutation_rate
    self.__num_crossover   = int((population_size * crossover_rate) / 2)
    self.__num_mutate      = int(population_size * mutation_rate)


    self.__population = [Genome(self.__genome_length) for i in range(self.__population_size)]

  # Evaluate each individual in the population
  def EvaluatePopulation(self):
    for individual in self.__population:
      val = sum(individual.getGenome())

      # Calculate fitness
      if (abs(val - self.__target) == 0):
        fitness = 1.0
      elif (abs(val - self.__target) == 1):
        fitness = 0.95
      else:
        fitness = 1.0 / float(abs(val - self.__target))

      individual.setFitness(fitness)
    return

  # Perform tournament selection to pick a random individual
  # Note here we don't necessarily distinguish between crossover or mutation -- everybody is viable for all
  def selectRandomIndividual(self):
    K = 3  # tournament size
    winner = self.__population[random.randint(0,len(self.__population)-1)]
    for i in range(1, K):
      challenger = self.__population[random.randint(0,len(self.__population)-1)]
      if (challenger.getFitness() > winner.getFitness()):
        winner = challenger

    # Return the tournament winner
    return winner
  

  def performCrossover(self, parent_1, parent_2):
    genome_1 = parent_1.getGenome()
    genome_2 = parent_2.getGenome()

    assert(len(genome_1) == len(genome_2)) # ensure we have the same size

    # Single-point crossover - let's pick a random index each time
    index = random.randint(1,len(genome_1)-1) 

    # Fill in the children
    child_genome_1 = []
    child_genome_2 = []

    # Split up the genome
    for i in range(len(genome_1)):

      if (i < index): # Copy directly up to the cut point 
        child_genome_1.append(genome_1[i])
        child_genome_2.append(genome_2[i])
      else: # Copy from other parent after cut point
        child_genome_2.append(genome_1[i])
        child_genome_1.append(genome_2[i])
    
    child_1 = Genome(self.__genome_length)
    child_1.setGenome(child_genome_1)
    child_2 = Genome(self.__genome_length)
    child_2.setGenome(child_genome_2)

    return child_1, child_2

  def performEvolutionaryOperations(self):
    new_population = []

    # Selection is embedded in each operation
    
    # Crossover
    for i in range(self.__num_crossover):
      # Perform parent selection
      parent_1 = self.selectRandomIndividual()
      parent_2 = self.selectRandomIndividual()
      while (parent_1 == parent_2):
        parent_2 = self.selectRandomIndividual()
      offspring = self.performCrossover(parent_1, parent_2)
      new_population.append(offspring[0])
      new_population.append(offspring[1])

    # Mutation
    for i in range(self.__num_mutate):
      # Perform mutant selection
      individual = self.selectRandomIndividual()
      # Create a copy to mutate
      mutant = copy.deepcopy(individual)
      # And mutate
      mutant.Mutate()
      new_population.append(mutant)

    # Fill in population
    while (len(new_population) < self.__population_size):
      new_population.append(Genome(self.__genome_length))

    return new_population # Return the next generation

  def Execute(self):
    for i in range(self.__num_generations):
   
      self.EvaluatePopulation()
      self.__population = self.performEvolutionaryOperations()

      # Sort population based on fitness
      self.__population.sort(key=lambda x: x.getFitness(), reverse=True)
      print("Generation: %d, Best: Fitness [%f], Indv %s" % (i, self.__population[0].getFitness(), self.__population[0].getGenome()))

      # Cull the herd if we have too many (already sorted)
      self.__population = self.__population[:self.__population_size]

    # Evaluate one final time
    self.EvaluatePopulation()

    # Sort population based on fitness
    self.__population.sort(key=lambda x: x.getFitness(), reverse=True)

    # Output the best genome and its fitness
    print("############################")
    print("Best individual: %s" % str(self.__population[0].getGenome()))
    print("Sum: [%d], Target: [%d]" % (sum(self.__population[0].getGenome()), self.__target))
    print("Fitness: [%f]" % self.__population[0].getFitness())
    print("############################")
   
  
# Main function     
if __name__ == "__main__":
 
  #random.seed(1)

  ga = GA(100, 20, 0.7, 0.2, 372, 5)
  ga.Execute()
