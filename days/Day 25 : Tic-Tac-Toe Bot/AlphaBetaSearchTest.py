from State import State
from AlphaBetaSearch import AlphaBetaSearch


initialState = State()
dfs = AlphaBetaSearch(initialState, 2, True)
dfs.search() 