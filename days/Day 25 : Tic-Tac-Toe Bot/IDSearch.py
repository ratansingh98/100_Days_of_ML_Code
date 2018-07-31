import Config
from AlphaBetaSearch import AlphaBetaSearch

class IDSearch:
    """
    This performs Iterative Deepening search
    """
    
    def __init__(self, boardValues, display):
        self.boardValues = boardValues
        self.display = display
    
    
    def search(self):
        """
        This method performs the search
        """      
        #best move found so far
        bestMove = None
        for currentDepth in range(Config.maximumDepth):
            #find best move for current depth
            abSearch = AlphaBetaSearch(self.boardValues, currentDepth, self.display)
            currentBestMove = abSearch.search()
            #assign if not none
            if currentBestMove != None:
                bestMove = currentBestMove
        print ("-- bestMove --", bestMove)
        return bestMove