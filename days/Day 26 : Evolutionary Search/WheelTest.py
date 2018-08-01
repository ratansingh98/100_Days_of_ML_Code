from EvolutionarySearch import EvolutionarySearch

nQueens = 8
evolSearch = EvolutionarySearch(nQueens, True, True)

evolSearch.fitness = [1, 2, 3, 4, 5, 5, 10, 20, 30, 20]
evolSearch.computeFitnessWheel()
print (evolSearch.wheel)

for i in range(10):
    evolSearch.selectParent()