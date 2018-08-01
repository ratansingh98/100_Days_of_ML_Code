import numpy as np
import random
import math
import matplotlib.pyplot as plt
import Config
import Data
import matplotlib.lines as mlines


class EvolutionarySearch:
    """
    This class deals with evolutionary search
    """
    
    def __init__(self, unique, debug): 
        
        #parameters
        self.nChromosomes = Data.nCities
        self.unique = unique
        self.debug = debug
        self.fitnessTrack = []
        self.generationCount = 100
        
        #initialize
        self.population = np.zeros((Config.populationSize, self.nChromosomes), np.int8)
        for i in range(Config.populationSize):
            if self.unique:
                array = np.arange(self.nChromosomes)
                np.random.shuffle(array)
            for j in range(self.nChromosomes):
                if not self.unique:
                    value = math.floor(self.nChromosomes * random.random())
                    self.population[i, j] = value
                else:
                    self.population[i, j] = array[j]


    def findIndividualFitness(self, individual):
        """
        This method finds the total distance travelled
        """
        #initialize
        distance = 0
        for index in range(1, Data.nCities):
            #get location of two cities
            location1 = Data.locationData[Data.cities[individual[index - 1]]]
            location2 = Data.locationData[Data.cities[individual[index]]]
            distance += math.sqrt((location1[0] - location2[0]) ** 2 + \
                                  (location1[1] - location2[1]) ** 2)
        return 1000.0/distance
    
    

    def computeFitness(self):
        """
        This method computes the fitness for the individuals
        """
        self.fitness = np.zeros((Config.populationSize, 1))
        
        for index in range(Config.populationSize):
            #individual
            individual = self.population[index, :]
            
            #find the fitness value
            self.fitness[index] = self.findIndividualFitness(individual)
            
            self.computeFitnessWheel()
        
        
    def computeFitnessWheel(self):
        """
        This method computes the fitness wheel
        """
    
        #compute fitness wheel
        self.wheel = np.zeros((Config.populationSize, 1))
        self.wheel[0] = self.fitness[0]
        for index in range(1, Config.populationSize):
            self.wheel[index] = self.wheel[index - 1] + self.fitness[index]
        total = self.wheel[Config.populationSize - 1]
        if self.debug:
            print ("total", total)
        self.wheel = self.wheel / total
           
        
    def selectParent(self):
        """
        This method selects a parent
        """
        #generate a random value
        rand = random.random()    
        if self.debug:
            print ("random value", rand)
        for index in range(Config.populationSize):
            if rand < self.wheel[index]:
                if self.debug:
                    print ("parent selected", index)
                return index 
           
        
    def crossOverParents(self, parent1, parent2):
        """
        This method crosses over parents to produce a child
        """
        #select a crossover point
        crossOverPoint = int(math.floor(self.nChromosomes * random.random()))
        if self.debug:
            print ("crossOverPoint", crossOverPoint)
        
        #get inherited part from parent1
        parent1Part = parent1[0 : crossOverPoint + 1]
        
        #get inherited part from parent2
        if not self.unique:
            parent2Part = parent2[crossOverPoint : ]
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
        #perform mutation
        for index in range(self.nChromosomes):
            rand = random.random()
            if rand < Config.mutationRate:
                if self.debug:
                    print ("mutating index", index)
                if not self.unique:
                    child[index] = int(math.floor(self.nChromosomes * random.random())) 
                else:
                    #select another index to switch this chromosome with
                    index2 = int(math.floor(self.nChromosomes * random.random())) 
                    child[index], child[index2] = child[index2], child[index]
        return child
    
    
    def getHallOfFame(self):
        """
        This method gets the hall of fame
        """
        #sort individuals in descending order of fitness
        sortedIndex = (np.squeeze(-self.fitness)).argsort()
        sortedIndividuals = self.population[sortedIndex]
        
        #get hallOfFameCount and store in hall of fame
        hallOfFame = sortedIndividuals[0 : Config.hallOfFameCount, :]
        return hallOfFame
        
        
    def performVariation(self):
        """
        This method performs crossover and mutation
        """
        newPopulation = np.zeros((Config.populationSize, self.nChromosomes), np.int8)
        
        #copy hall of fame
        hallOfFame = self.getHallOfFame()
        for index in range(Config.hallOfFameCount):
            newPopulation[index, :] = hallOfFame[index, :]
        
        
        for index in range(Config.hallOfFameCount, Config.populationSize):
            #select two parents
            pIndex1 = self.selectParent()
            pIndex2 = self.selectParent()
            parent1 = self.population[pIndex1, :]
            parent2 = self.population[pIndex2, :]
            
            #check if we will crossover
            rand = random.random()    
            if rand < Config.crossoverRate:
                child = self.crossOverParents(parent1, parent2)
                
            else:
                #select the best parent
                if self.fitness[pIndex1] > self.fitness[pIndex2]:
                    child = parent1
                else:
                    child = parent2
                    
            #mutate
            child = self.mutateChild(child)       
            
            #fill child in new population
            newPopulation[index, :] = child
            
        #replace old population
        self.population = newPopulation
        
    
    def drawSolution(self, solution):
        """
        This method draws the solution
        """
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
      
        for i in range(1, self.nChromosomes):
            location1 = Data.locationData[Data.cities[solution[i - 1]]]
            location2 = Data.locationData[Data.cities[solution[i]]]
            l = mlines.Line2D([location1[0],location2[0]], [location1[1],location2[1]])
            ax.add_line(l)
        
        for i in range(self.nChromosomes):
            location = Data.locationData[Data.cities[solution[i]]]
            cir = plt.Circle((location[0], location[1]), 0.4, color = "blue")
            ax.add_patch(cir)
            ax.text(location[0] + 0.5, location[1] + 0.5, Data.cities[solution[i]])
        
        ax.axis([0, 9, 0, 9])
        plt.grid()
        plt.show()   
        
        
    def findBestSolution(self):
        """
        This method finds the best solution and its fitness
        """
        maxFitnessIndex = np.argmax(self.fitness)
        maxFitnessValue = self.fitness[maxFitnessIndex][0]
        self.fitnessTrack.append(maxFitnessValue)
        return self.population[maxFitnessIndex], maxFitnessValue
    
        
    def checkStopSearching(self, bestFitness):
        """
        This method tells to stop searching when the last 5 fitness are same
        """
        if self.generationIndex < 20:
            return False
        
        uniqueLast5Values = set(self.fitnessTrack[-20:])
        if len(uniqueLast5Values) == 1 and bestFitness in uniqueLast5Values:
            return True
        else:
            return False
        
        
    def search(self):
        """
        This method finds the best solution 
        """
        
        #initialize
        bestSolution = None
        bestFitness = 0
        
        #find fitness 
        self.computeFitness()
        
        #generation
        for self.generationIndex in range(self.generationCount):
            
            #generate new population by crossover and mutation
            self.performVariation()
            
            #recalculate fitness
            self.computeFitness()
            
            #update best solution  
            bestSolution1, maxFitnessValue = self.findBestSolution()
            print( maxFitnessValue)
            if maxFitnessValue > bestFitness:
                bestSolution = bestSolution1
                bestFitness = maxFitnessValue
                
            #check if we need to stop searching
            if self.checkStopSearching(maxFitnessValue):
                break
            
        print (self.generationIndex , bestSolution, bestFitness)
        self.drawSolution(bestSolution) 