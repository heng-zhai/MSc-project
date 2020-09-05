"""
MSc Project
Enhanced bees algorithm
Mainly focus on the reduction of parameters
Author: Heng Zhai
"""

import random
import copy

class Bee(object):
    def __init__(self, lowerBoundaries, upperBoundaries, shrinkTimes, patchSize, isScout=True, centre=None):
        self.lowerBoundaries = lowerBoundaries
        self.upperBoundaries = upperBoundaries
        self.position = []
        self.shrinkTimes = shrinkTimes
        self.patchSize = patchSize
        self.fitness = None
        if centre == None:
            centre=[(upperBoundaries[i] + lowerBoundaries[i]) / 2.0 for i in range(len(lowerBoundaries))]
        if isScout:
            self.initialiseValues([1.0]*len(lowerBoundaries), centre=centre)
        else:
            self.initialiseValues(patchSize, centre=centre)

    # Randomly initialize the position of the bee in the n-dimensional hyper box    
    def initialiseValues(self, patchSize, centre):
        self.position = [0.0] * len(self.lowerBoundaries)
        for i in range(len(self.lowerBoundaries)):
            middle = (self.upperBoundaries[i] - self.lowerBoundaries[i]) / 2.0
            self.position[i] = random.uniform(-middle, middle) * patchSize[i] + centre[i]
            self.position[i] = min(self.position[i], self.upperBoundaries[i])
            self.position[i] = max(self.position[i], self.lowerBoundaries[i])

    # Generate single recruit in the neighbourhood range
    def generateRecruit(self):
	    return Bee(self.lowerBoundaries,self.upperBoundaries,0,self.patchSize,isScout=False,centre=self.position)

    # Use this method to complete the comparison between Bee objects
    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        return "Bee{" + "fitness: " + str(self.fitness)+", position: "+str(self.position) + "}"
        

class EnhancedBA(object):
    def __init__(self, fitnessFunction, lowerBoundaries, upperBoundaries, ngh=None, ns=35, nb=8, nr=80, sf=.2, stlim=10):
        self.ns = ns
        self.nb = nb
        self.nr = nr
        self.fitnessFunction = fitnessFunction
        self.lowerBoundaries = lowerBoundaries
        self.upperBoundaries = upperBoundaries
        if ngh == None:
            self.ngh = [1.0]*len(lowerBoundaries)
        else:
            self.ngh = ngh
        self.stlim = stlim
        self.sf = sf
        self.currentSites = []
        self.keep_bees_trace = False
        self.bestSolution = None
        self.record = []
        self.checkParameters()
        self.initialise_solution()

    # Check whether the provided parameters are valid
    def checkParameters(self):
        # The lengths of lower boundaries and upper boundaries should be equal
        if len(self.lowerBoundaries) != len(self.upperBoundaries):
            raise ValueError("The sizes of the lower and upper bounds don't match")
        # The number of best sites should be greater than or equal to 2 so that the tournament selection can run normally
        if self.nb < 2:
            raise ValueError("The number of best sites should be greater than or equal to 2")
        # The value range of shrink factor should be [0, 1]
        if self.sf < 0 or self.sf > 1:
            raise ValueError("The shrink factor should be greater than 0 and less than 1")
        
    # A number of ns scout bees are randomly scattered across the solution space in the initial stage
    def initialise_solution(self):
        self.currentSites = [self.generate_scout() for _ in range(self.ns)]
        self.currentSites.sort(reverse=True)
        self.currentSites = self.currentSites[:self.nb]
        self.bestSolution = self.currentSites[0]
        
    # Use tournament selection to allocate recruits to each selected site
    # The whole process of the waggle dance:
    # 1. Random pick two sites from selected sites (we assume that the recruits are uniformly distributed in the hive
    # and due to the limitation of the individual’s vision, each recruit will only choose the two scout bees closest 
    # to it for comparison by viewing the waggle dance)
    # 2. Let each recruit evaluate the fitness of these two sites
    # 3. The recruit will choose the best one to follow (append the index of best one to recruits choices list)
    # 4. Count the total number of recruits for each selected site
    def waggle_dance(self):
        n_recruits = 1
        recruits_choices = []
        for i in range(self.nr):
            randIndex = random.sample(range(0, self.nb), 2)
            if randIndex[0] < randIndex[1]:
                recruits_choices.append(randIndex[0])
            else:
                recruits_choices.append(randIndex[1])

        for j in range(self.nb):
            if recruits_choices.count(j) > 0:
                n_recruits = recruits_choices.count(j)
            self.localSearchForSingleSite(j, n_recruits)
    
    # Local search for single site
    def localSearchForSingleSite(self, index, n_recruits):
        if self.currentSites[index].shrinkTimes == self.stlim:
            # Abandon this site
            scouts = [self.generate_scout() for _ in range(n_recruits)]
            scouts.sort(reverse=True)
            self.currentSites[index] = copy.deepcopy(scouts[0])
        else:
            # Assign specific number of recruited bees for this site
            recruits = [self.generate_recruit(self.currentSites[index]) for _ in range(n_recruits)]
            if self.keep_bees_trace:
                self.to_save_recruits += [recruits]
            # Get the best recruit
            bestRecruit = self.argmax(recruits)
            if bestRecruit.fitness > self.currentSites[index].fitness:
                # If the solution can be improved continuously
                # 1. The best recruit becomes the new scout bee of this site
                # 2. Reset the shrink times of this site to 0
                self.currentSites[index] = copy.deepcopy(bestRecruit)
                self.currentSites[index].shrinkTimes = 0
            else:
                # If no improvement can be obtained
                # 1. Increase the shrink times of this site by 1
                # 2. Adjust the size of the neighbourhood
                self.currentSites[index].shrinkTimes += 1
                self.currentSites[index].patchSize = [x * (1 - self.sf) for x in self.currentSites[index].patchSize]
    
    def singleIteration(self):
        if self.keep_bees_trace:
            self.to_save_best_sites = [copy.deepcopy(x) for x in self.currentSites]
            self.to_save_recruits= []
        self.waggle_dance()
        # Add (ns - nb) scouts to the search space
        self.currentSites += [self.generate_scout() for _ in range(self.ns - self.nb)]
        # Sort the current sites in descending order
        self.currentSites.sort(reverse=True)
        # The first nb sites become new current sites
        self.currentSites = self.currentSites[:self.nb]
        # Update best solution if the fitness of the first site in current sites is better
        if self.currentSites[0].fitness > self.bestSolution.fitness:
            self.bestSolution = copy.deepcopy(self.currentSites[0])
        self.record.append(self.bestSolution.fitness)

    # Determine whether the maximum number of iterations or the acceptable fitness is reached
    def stoppingCriterion(self, max_iteration=None, max_fitness=None):
        if max_iteration == None and max_fitness == None:
            raise ValueError("Please provide a stop criteria")
        if max_iteration != None and max_iteration < 0:
            raise ValueError("The maximum number of iterations should be positive")
        iteration = 0
        while(max_iteration == None or iteration < max_iteration) and (max_fitness == None or self.bestSolution.fitness < max_fitness):
            self.singleIteration()
            iteration += 1
        return iteration, self.bestSolution.fitness

    # Generate single scout bees in the search space
    def generate_scout(self):
        scout = Bee(self.lowerBoundaries, self.upperBoundaries, 0, self.ngh, isScout=True, centre=None)
        scout.fitness = self.fitnessFunction(scout.position)
        return scout

    # Generate single recruit for specific selected site
    def generate_recruit(self, site):
        recruit = site.generateRecruit()
        recruit.fitness = self.fitnessFunction(recruit.position)
        return recruit

    # Get the best solution
    def argmax(self, solutions):
        bestSolution = None
        for solution in solutions:
            if bestSolution == None or solution.fitness > bestSolution.fitness:
                bestSolution = solution
        return bestSolution