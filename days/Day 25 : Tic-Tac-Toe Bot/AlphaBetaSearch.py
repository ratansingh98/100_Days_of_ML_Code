from Node import Node
from TreePlot import TreePlot


class AlphaBetaSearch:
    """
    This class performs alpha beta search
    """
    
    def __init__(self, currentState, currentMaxDepth, display):
        self.currentMaxDepth = currentMaxDepth
        self.display = display
        self.currentState = currentState
        
    
    def search(self):
        """
        This method performs the search
        """
        #create root node
        rootNode = Node(self.currentState, None)
        
        #initialize parameters for minimax search
        maxPlayerFlag = True
        playerIndex = 0
        depth = self.currentMaxDepth
        alpha = -float("inf")
        beta = float("inf")
        
        #perform alpha beta search from root node
        bestScore = self.alphaBetaSearch(rootNode, depth, maxPlayerFlag, playerIndex, 
                                 alpha, beta)
        
        #find the first level child with the score
        bestMove = rootNode.getBestMove(bestScore)
        
        if self.display:            
            treePlot = TreePlot()
            treePlot.generateDiagram(rootNode, bestMove)

        return bestMove
        
    
    def alphaBetaSearch(self, node, depth, maxPlayerFlag, playerIndex, alpha, beta):
        """
        This creates the search tree
        """
        if depth == 0:
            #if depth is 0, then return the score for the board state
            node.score = node.evaluateState()
            return node.score
        else:            
            #find the successor states from current state 
            childStates, moves = node.state.successorFunction(playerIndex)
            
            #if there is no child, then evaluate the node
            #if we have reached winning/losing/draw state
            if len(childStates) == 0:
                node.score = node.state.evaluateState()
                return node.score
            
            #add these states as children nodes of current node
            for index in range(len(childStates)):
                childState, move = childStates[index], moves[index]
                childNode = Node(childState, move)
                
                #add child
                node.addChild(childNode)
                
                #get child node's score
                childScore = self.alphaBetaSearch(childNode, depth - 1, 
                                                  not maxPlayerFlag,
                                                  1 - playerIndex, 
                                                  alpha, beta)
                
                #find maximum/minimum based on maxPlayerFlag
                if maxPlayerFlag:
                    #update alpha, score
                    alpha = max(alpha, childScore)
                    node.score = alpha
                    if beta <= alpha:
                        return alpha
                else:
                    #update beta, score
                    beta = min(beta, childScore)
                    node.score = beta
                    if beta <= alpha:
                        return beta   
                    
            #set the alpha and beta of the node
            node.alpha = alpha
            node.beta = beta
            
            #return alpha/beta
            if maxPlayerFlag:    
                return alpha
            else:
                return beta     