from EvolutionarySearch import EvolutionarySearch

nQueens = 8
evolSearch = EvolutionarySearch(nQueens, True, True)

parent1 = [0, 1, 2, 3, 4, 5, 6, 7]
parent2 = [7, 6, 5, 4, 3, 2, 1, 0]
child = evolSearch.crossOverParents(parent1, parent2)
print (child)