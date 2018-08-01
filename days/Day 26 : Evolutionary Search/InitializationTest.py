from EvolutionarySearch import EvolutionarySearch

nQueens = 8
evolSearch = EvolutionarySearch(nQueens, True, True)
print (evolSearch.population)

#draw first individual of population
individual = evolSearch.population[0, :]
evolSearch.drawIndividual(individual)
