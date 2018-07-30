from State import State

initialState = State()
intermediateState1 = State(initialState.assignment, initialState.possibleValues,
                          "state1", "red")
intermediateState2 = State(intermediateState1.assignment, 
                           intermediateState1.possibleValues, "state2", "red")
intermediateState3 = State(intermediateState2.assignment, 
                           intermediateState2.possibleValues, "state3", "green")
intermediateState4 = State(intermediateState3.assignment, 
                           intermediateState3.possibleValues, "state4", "blue")
print (intermediateState4.forwardCheck())