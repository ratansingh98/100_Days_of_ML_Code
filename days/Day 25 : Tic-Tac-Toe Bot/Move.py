class Move:
    """
    Class representing a move made by a player on the board 
    """
    
    def __init__(self, row, col, playerValue):
        self.row = row
        self.col = col
        self.playerValue = playerValue