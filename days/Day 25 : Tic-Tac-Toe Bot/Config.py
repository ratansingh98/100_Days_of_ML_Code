#Game parameters

#the number of squares along the length and breadth of the board
nSquares = 3

#text for the moves (to be used in GUI)
moveTexts = ["X", "O"]

#which player goes first, startPlayer = 0 (computer), 1 (human)
#define player order
startPlayer = 0
if startPlayer == 0:
    computerPlayer = 0
    humanPlayer = 1
else:
    humanPlayer = 0
    computerPlayer = 1
#winner will use the same player value

#when draw state has been reached
drawValue = 2

#maximum depth
maximumDepth = 5