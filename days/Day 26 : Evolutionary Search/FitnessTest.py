from EvolutionarySearch import EvolutionarySearch

nQueens = 8
individual = [4, 5, 6, 3, 4, 5, 6, 5]

evolSearch = EvolutionarySearch(nQueens, False, True)
print (evolSearch.computeIndividualFitness(individual))
evolSearch.drawIndividual(individual)