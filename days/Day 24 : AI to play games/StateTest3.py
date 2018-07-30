from State import State

initialState = State()
intermediateState = State(initialState.assignment, initialState.possibleValues,
                          "state1", "red")
intermediateState = State(intermediateState.assignment, intermediateState.possibleValues,
                          "state2", "red")
intermediateState = State(intermediateState.assignment, intermediateState.possibleValues,
                          "state3", "green")
print (intermediateState.arcConsistency())