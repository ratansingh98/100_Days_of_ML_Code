from EvolutionarySearch import EvolutionarySearch

nQueens = 8
evolSearch = EvolutionarySearch(nQueens, True, True)

child = [0, 1, 2, 3, 4, 5, 6, 7]
child = evolSearch.mutateChild(child)
print (child)