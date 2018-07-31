import Config
import numpy as np
from Move import Move

class State:
    '''
    This class retrieves state information for search application
    '''
    
    def __init__(self, boardValues = None):
        if boardValues is None:
            #create initial state
            self.boardValues = self.getInitialState()
        else:
            self.boardValues = boardValues
            
    
    def getInitialState(self):
        """
        This method returns a numpy array of size 3x3 filled with -1 
        """
        initialState = -1 * np.ones((Config.nSquares, Config.nSquares), np.int8)
        return initialState
    
    
    def checkGoalState(self):
        """
        This method checks whether a winning/lose/draw position has been reached 
        """ 
        #initialize
        winner = -1
        endFlag = False
        
        #all the lines passing through different squares
        #each row consists of 3 squares, in the form of row, col
        lineCoordinates = [[0, 0, 0, 1, 0, 2],
                           [1, 0, 1, 1, 1, 2],
                           [2, 0, 2, 1, 2, 2],
                           [0, 0, 1, 0, 2, 0],
                           [0, 1, 1, 1, 2, 1],
                           [0, 2, 1, 2, 2, 2],
                           [0, 0, 1, 1, 2, 2],
                           [0, 2, 1, 1, 2, 0]]
        #for all lines
        for lineIndex in range(len(lineCoordinates)):
            #get the 3 square values
            row1 = lineCoordinates[lineIndex][0]
            col1 = lineCoordinates[lineIndex][1]
            row2 = lineCoordinates[lineIndex][2]
            col2 = lineCoordinates[lineIndex][3]
            row3 = lineCoordinates[lineIndex][4]
            col3 = lineCoordinates[lineIndex][5]
            squareValue1 = self.boardValues[row1, col1]
            squareValue2 = self.boardValues[row2, col2]
            squareValue3 = self.boardValues[row3, col3]
            
            #if they are the same and not -1
            if squareValue1 != -1 and squareValue1 == squareValue2 and \
                squareValue2 == squareValue3:
                #find the winner
                if squareValue1 == Config.computerPlayer:
                    winner = Config.computerPlayer
                    endFlag = True
                    return endFlag, winner
                if squareValue1 == Config.humanPlayer:
                    winner = Config.humanPlayer
                    endFlag = True
                    return endFlag, winner
                
        #check if all squares occupied
        for i in range(Config.nSquares):
            for j in range(Config.nSquares):
                #if there is one square which is not occupied, return False
                if self.boardValues[i, j] == -1:
                    return endFlag, winner
                
        #if all squares are occupied, then game is a draw
        winner = Config.drawValue
        endFlag = True
        return endFlag, winner
    
    
    def checkSameStates(self, boardValues1, boardValues2):
        """
        This method returns true if two states are same
        """
        #find the number of elements which are same
        sameCount = np.sum(boardValues1 == boardValues2)
        #if this total is same as number of squares in the board
        return sameCount == Config.nSquares * Config.nSquares
    
    
    def checkSymmetry(self, boardValues1, boardValues2):
        """
        This method checks if two board states are symmetric
        """        
        #1. check if there is rotation symmetry
        rotBoardValues = np.copy(boardValues1)
        for _ in range(3):
            rotBoardValues = np.rot90(rotBoardValues)
            if self.checkSameStates(rotBoardValues, boardValues2):
                return True
        
        #2. check if there is reflection symmetry
        #2.1 flip left right for horizontal reflection
        flipBoardValues = np.copy(boardValues1)
        flipBoardValues = np.fliplr(flipBoardValues)
        if self.checkSameStates(flipBoardValues, boardValues2):
            return True
        
        #2.2 flip up down for vertical reflection
        flipBoardValues = np.copy(boardValues1)
        flipBoardValues = np.flipud(flipBoardValues)
        if self.checkSameStates(flipBoardValues, boardValues2):
            return True
        
        #3. check if there is a reflection symmetry along diagonals
        #3.1 reflection along primary diagonal
        mirrorBoardValues = np.copy(boardValues1)
        mirrorBoardValues = np.swapaxes(mirrorBoardValues, 0, 1)
        if self.checkSameStates(mirrorBoardValues, boardValues2):
            return True
        
        #3.2 reflection along secondary diagonal
        mirrorBoardValues = np.copy(boardValues1)
        #rotate 180
        mirrorBoardValues = np.rot90(mirrorBoardValues)
        mirrorBoardValues = np.rot90(mirrorBoardValues)
        mirrorBoardValues = np.swapaxes(mirrorBoardValues, 0, 1)
        if self.checkSameStates(mirrorBoardValues, boardValues2):
            return True
        
        return False


    def createChildState(self, move):
        """
        This method creates a child state when a move is made from current state
        """
        boardValues = np.copy(self.boardValues)
        boardValues[move.row][move.col] = move.playerValue
        newChildState = State(boardValues)
        return newChildState
        

    def successorFunction(self, playerValue):
        """
        This is the successor function. It generates all the possible
         moves that playerValue can play from current board state. Then it returns the states
         with those moves. It considers only non-symmetric child states.
        """
        
        #check if it is a winning/losing/draw state
        endFlag, _ = self.checkGoalState()
        if endFlag:
            return [], []
        
        #initialize
        childStates = []
        moves = []
        
        #first find all the moves possible
        for row in range(Config.nSquares):
            for col in range(Config.nSquares):
                #check if the square is occupied
                if self.boardValues[row, col] == -1:
                    #move
                    move = Move(row, col, playerValue)
                    #then create a child state with that move
                    newChildState = self.createChildState(move)
                    
                    #before adding child state, check if it is symmetric with any
                    # other child state
                    symmetricFlag = False
                    for childState in childStates:
                        if self.checkSymmetry(newChildState.boardValues,
                                              childState.boardValues):
                            symmetricFlag = True
                    #add new child state if it is not symmetric with others
                    if not symmetricFlag:        
                        childStates.append(newChildState)
                        moves.append(move)
        return childStates, moves
        
    
    def evaluateState(self):
        """
        This method evaluates the board state and returns a score for it
        """
        
        
                      
        #initialize score
        score = 0
        #all the lines passing through different squares
        #each row consists of 3 squares, in the form of row, col
        lineCoordinates = [[0, 0, 0, 1, 0, 2],
                           [1, 0, 1, 1, 1, 2],
                           [2, 0, 2, 1, 2, 2],
                           [0, 0, 1, 0, 2, 0],
                           [0, 1, 1, 1, 2, 1],
                           [0, 2, 1, 2, 2, 2],
                           [0, 0, 1, 1, 2, 2],
                           [0, 2, 1, 1, 2, 0]]
        #scores for different amount of marks along a line
        scores = [0,
                  1,
                  10,
                  100]
        #for each line
        for lineIndex in range(len(lineCoordinates)):
            #count own and opponents marks along a line
            pointsOnLine = 0
            opponentPointsOnLine = 0
            #for each square along a line
            for pointIndex in range(Config.nSquares):
                #find row, col
                row = lineCoordinates[lineIndex][2 * pointIndex]
                col = lineCoordinates[lineIndex][2 * pointIndex + 1]
                if self.boardValues[row, col] == Config.computerPlayer:
                    pointsOnLine += 1
                if self.boardValues[row, col] == Config.humanPlayer:
                    opponentPointsOnLine += 1
            #add subscore for each line
            score += scores[pointsOnLine] - scores[opponentPointsOnLine]
        return score  