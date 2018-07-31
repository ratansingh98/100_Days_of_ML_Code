import Config

class Node:
    '''
    This class represents a node in the search tree
    '''
    
    def __init__(self, state, move):
        """
        Constructor
        """
        self.state = state
        self.depth = 0
        self.children = []
        self.parent = None
        self.move = move
        self.score = 0
        self.alpha = -float("inf")
        self.beta = float("inf")
        
        
    def addChild(self, childNode):
        """
        This method adds a node under another node
        """
        self.children.append(childNode)
        childNode.parent = self
        childNode.depth = self.depth + 1
        
    
    def printTree(self):
        """
        This method prints the tree
        """
        print (self.depth , " - " , self.state.boardValues, " : ", self.score)
        for child in self.children:
            child.printTree()
            
            
    def getBestMove(self, bestScore):
        """
        This method is called on the root node
        This method returns the move of the child node with the score as bestScore
        """
        for child in self.children:
            if child.score == bestScore:
                #get the move responsible for this node
                print ("selected move", child.move.row, child.move.col)
                return child.move
            
            
    def evaluateState(self):
        """
        This method evaluates score of the node
        """
        return (Config.maximumDepth - self.depth + 1) * self.state.evaluateState()