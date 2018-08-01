import numpy as np
import random
import math
import matplotlib.pyplot as plt
import Config


class EvolutionarySearch:
    """
    This class deals with evolutionary search
    """
    
    def __init__(self, nChromosomes, unique, display): 
        
        #parameters
        self.nChromosomes = nChromosomes
        self.unique = unique
        self.display = display
        
        #initialize
        self.population = np.zeros((Config.populationSize, self.nChromosomes), \
                                   np.int8)
        #for each individual
        for i in range(Config.populationSize):
            if self.unique:
                array = np.arange(self.nChromosomes)
                np.random.shuffle(array)
            #for each chromosome
            for j in range(self.nChromosomes):
                if not self.unique:
                    value = math.floor(self.nChromosomes * random.random())
                    self.population[i, j] = value
                else:
                    self.population[i, j] = array[j]
                


    def drawIndividual(self, individual):
        """
        This method draws the individual
        """
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        colors = ["black", "white"]
        
        #draw black white chess board
        for i in range(self.nChromosomes):
            cIndex = i % 2
            for j in range(self.nChromosomes):
                rect = plt.Rectangle((i,j), 1, 1, color=colors[cIndex])
                cIndex = 1 - cIndex
                ax.add_patch(rect)
        #draw n queens
        for i in range(self.nChromosomes):    
            cir = plt.Circle((individual[i] + 0.5, i + 0.5), 0.4, color = "blue")
            ax.add_patch(cir)
      
        ax.axis([0, self.nChromosomes, 0, self.nChromosomes])
        plt.title(str(individual))
        plt.grid()
        plt.show()   


    def computeIndividualFitness(self, individual):
        """
        This method computes fitness of an individual
        Fitness = max attacks - number of attacks + 1
        """
        #initialize
        nAttacks = 0
        #for index1
        for index1 in range(self.nChromosomes):
            #for index2
            for index2 in range(index1 + 1, self.nChromosomes):
                #check if the values at these two chromosomes creates an attack
                
                #check if they are in the same column
                if individual[index1] == individual[index2]:
                    nAttacks += 1
                    if self.display:
                        print ("same column", index1, index2)
                        
                #check if they are in diagonal
                difference1 = index2 - index1
                difference2 = math.fabs(individual[index2] - individual[index1])
                if difference1 == difference2:
                    nAttacks += 1
                    if self.display:
                        print ("diagonal", index1, index2, \
                            individual[index1], individual[index2])
        return Config.maxFitness - nAttacks
    

    def computePopulationFitness(self):
        """
        This method computes the fitness for the population
        """
        self.fitness = np.zeros((Config.populationSize, 1))
        
        #for each individual
        for index in range(Config.populationSize):
            #individual
            individual = self.population[index, :]
            
            #find the fitness value
            self.fitness[index] = self.computeIndividualFitness(individual)
            
            self.computeFitnessWheel()
        
        
    def computeFitnessWheel(self):
        """
        This method computes the fitness wheel
        """
    
        #initialize
        self.wheel = np.zeros((Config.populationSize, 1))
        self.wheel[0] = self.fitness[0]
        
        for index in range(1, Config.populationSize):
            self.wheel[index] = self.wheel[index - 1] + self.fitness[index]
        
        #last value of wheel
        lastValue = self.wheel[Config.populationSize - 1]
        if self.display:
            print ("lastValue", lastValue)
        self.wheel = self.wheel / lastValue
        
        
    def selectParent(self):
        """
        This method selects a parent using fitness wheel
        """
        #generate a random value
        rand = random.random()    
        for index in range(Config.populationSize):
            #find first value of wheel greater than or equal to random number
            if self.wheel[index] >= rand:
                if self.display:
                    print ("parent selected", index)
                return index 
           
        
    def crossOverParents(self, parent1, parent2):
        """
        This method crosses over parents to produce a child
        """
        #select a crossover point
        crossOverPoint = int(math.floor(self.nChromosomes * random.random()))
        if self.display:
            print ("crossOverPoint", crossOverPoint)
        
        #get inherited part from parent1
        parent1Part = parent1[0 : crossOverPoint + 1]
        
        #get inherited part from parent2
        if not self.unique:
            parent2Part = parent2[crossOverPoint + 1: ]
        else: 
            #remove those numbers from parent2
            parent2Part = np.copy(parent2)
            for index in range(len(parent1Part)):
                index2 = np.argwhere(parent2Part==parent1Part[index])
                parent2Part = np.delete(parent2Part, index2)  
        #create a child        
        child = np.concatenate((parent1Part, parent2Part))    
        
        return child
        
    
    def mutateChild(self, child):
        """
        This method mutates child
        """
        #for each chromosome
        for index in range(self.nChromosomes):
            rand = random.random()
            #check if we will mutate this chromosome
            if rand < Config.mutationRate:
                
                if not self.unique:
                    if self.display:
                        print ("mutating index", index)
                    child[index] = int(math.floor(self.nChromosomes * \
                                                  random.random())) 
                else:
                    #select another chromosome to switch this chromosome with
                    index2 = int(math.floor(self.nChromosomes * random.random())) 
                    if self.display:
                        print( "mutating index", index, "with", index2)
                    child[index], child[index2] = child[index2], child[index]
        return child
        
        
    def performVariation(self):
        """
        This method uses crossover and mutation to create a new population
        """
        #initialize
        newPopulation = np.zeros((Config.populationSize, self.nChromosomes), \
                                 np.int8)
        
        for index in range(Config.populationSize):
            #select two parents' indexes
            pIndex1 = self.selectParent()
            pIndex2 = self.selectParent()
            parent1 = self.population[pIndex1, :]
            parent2 = self.population[pIndex2, :]
            
            #check if we will crossover
            rand = random.random()    
            if rand < Config.crossoverRate:
                child = self.crossOverParents(parent1, parent2)
                
            else:
                #select the fitter parent
                if self.fitness[pIndex1] > self.fitness[pIndex2]:
                    child = parent1
                else:
                    child = parent2
                    
            #mutate
            child = self.mutateChild(child)       
            
            #fill child in new population
            newPopulation[index, :] = child
            
        #replace old population with new population
        self.population = newPopulation
        
        
    def checkBestSolution(self):
        """
        This method finds whether we have encountered a solution
        """
        #initialize
        solution = None
        found = False
        #find index of maximum fitness value
        maxFitnessIndex = np.argmax(self.fitness)
        #find maximum fitness value
        maxFitnessValue = self.fitness[maxFitnessIndex]
        #check if solution
        if maxFitnessValue == Config.maxFitness:
            found = True
            solution = self.population[maxFitnessIndex, :]
               
        return found, solution
    
        
    def search(self):
        """
        This method finds the best solution using evolutionary search 
        """
        #init() has created a initial population
        
        #find fitness 
        self.computePopulationFitness()
        
        #generation
        self.generationCount = 0
        while True:
            
            #check if we have found solution
            found, solution = self.checkBestSolution()
                
            if found:
                print ("found solution")
                print( self.generationCount , solution)
                self.drawIndividual(solution)
                break               
                
            #generate new population by crossover and mutation
            self.performVariation()
            
            #recalculate fitness
            self.computePopulationFitness()
            
            self.generationCount += 1