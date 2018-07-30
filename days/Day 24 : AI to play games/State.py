import CSP
import collections
import numpy as np
import copy
from collections import deque


class State:
    '''
    This class retrieves state information for search application
    '''
    
    def __init__(self, assignment = None, possibleValues = None,
                 variable = None, value = None):
        if assignment == None:
            #create initial state
            self.assignment = self.getInitialState()
            #possibleValues has all the values for all variables
            self.possibleValues = collections.OrderedDict() 
            for variable in CSP.variables:
                self.possibleValues[variable] = copy.deepcopy(CSP.domainValues)
        else:
            assignment1 = copy.deepcopy(assignment)
            assignment1[variable] = value
            self.assignment = assignment1
            
            #assign value to variable's possible value
            possibleValues1 = copy.deepcopy(possibleValues)
            possibleValues1[variable] = [value]

            #remove value from variable's neighbours
            for neighbour in CSP.constraints[variable]:
                #the variable shouldn't have already been assigned
                if neighbour not in self.assignment:
                    if value in possibleValues1[neighbour]:
                        possibleValues1[neighbour].remove(value)
            #print possibleValues1
            self.possibleValues = possibleValues1
            
    
    def getInitialState(self):
        """
        This method returns empty assignment
        """
        return collections.OrderedDict() 
       

    def selectUnassignedVariable(self):
        """
        This method returns one variable which has not been assigned
        """
        #find first variable in CSP which is not present in assignment
        for variable in CSP.variables:
            if variable not in self.assignment:
                return variable
            
            
    def orderDomainValues(self):
        """
        This method returns the values in a particular order
        """
        return CSP.domainValues
    
        
    def checkGoalState(self):
        """
        This method checks whether the path is goal state 
        """ 
        #check if all the variables have been assigned
        
        #check the length of the dictionary
        if len(self.assignment) == len(CSP.variables):
            return True
        else:
            return False
        
    
    def drawState(self):
        """
        This method draws the state
        """
        image = np.zeros((7, 7, 3), np.uint8)
        for key in self.assignment.keys():
            #find the channel index
            if self.assignment[key] == "red":
                channelIndex = 0
            elif self.assignment[key] == "green":
                channelIndex = 1
            else:
                channelIndex = 2
            for indexes in CSP.positions[key]: 
                image[indexes[0], indexes[1], channelIndex] = 255
        return image
    

    def drawPossibleValues(self):
        """
        This method draws the possible values array
        """
        #create an array of size #variables X 3 X 3
        image = np.zeros((len(CSP.variables), 3, 3), np.uint8)
        
        #for all variables
        for key in self.possibleValues.keys():
            index = CSP.variables.index(key)
            #depending on colours fill the appropriate channels
            if "red" in self.possibleValues[key]:
                image[index, 0, 0] = 255
            if "green" in self.possibleValues[key]:
                image[index, 1, 1] = 255
            if "blue" in self.possibleValues[key]:
                image[index, 2, 2] = 255
        return image
    
    
    def forwardCheck(self):
        """
        This method performs forward checking
        It returns false when a variable has no possible values
        """
        for values in self.possibleValues.values():
            if len(values) == 0:
                return False
        return True
        
        
    def getConstraintsQueue(self):
        """
        This method returns a queue of constraint pairs
        """
        #initialize queue
        queue = []
        #for all variables
        for key in CSP.variables:
            #for all neighbours
            for neighbour in CSP.constraints[key]:
                if [neighbour, key] not in queue:
                    queue.append([key, neighbour])
        return queue
        
        
    def removeValues(self, possibleValues, variable1, variable2):
        """
        This method removes inconsistent values
        """
        #initialize
        removed = False
        #get possible values for both variables
        possibleValues1 = possibleValues[variable1]
        possibleValues2 = possibleValues[variable2]  
        for value1 in possibleValues1:
            satisfyCount = 0
            for value2 in possibleValues2:
                #check if these values are same
                if value1 != value2:
                    satisfyCount += 1
            #check if there is atleast one value of variable2 which satisfies
            # constraints for value1 of variable1
            if satisfyCount == 0:
                #remove value1 from variable1's possible values
                possibleValues[variable1].remove(value1) 
                removed = True
                print ("removed" , variable1, variable2, value1, " : ", removed)
        return removed
            
        
    def arcConsistency(self):
        """
        This methods checks if there would be an early failure using arc consistency
        """
        #initialize queue with constraints
        queue = deque(copy.deepcopy(self.getConstraintsQueue()))
        print ("queue", queue)
        
        #copy the possible values
        possibleValues = copy.deepcopy(self.possibleValues)
        print ("possibleValues", possibleValues)
        
        #process all constraints
        while len(queue) > 0:
            #check if the length of possible values for any variable is zero
            for variable in CSP.variables:
                if len(possibleValues[variable]) == 0:
                    print ("no possible values for a variable", variable)
                    return False

            #get first entry from queue
            (variable1, variable2) = queue.popleft()  
            print (variable1, variable2)

            #check if the pair is inconsistent
            if self.removeValues(possibleValues, variable1, variable2):
                #get the neighbours of variable1
                for neighbour in CSP.constraints[variable1]:
                    if neighbour != variable2:
                        print ("adding neighbour", (neighbour, variable1))
                        queue.append((neighbour, variable1))
                    
        return True