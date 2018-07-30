from State import State
import matplotlib.pyplot as plt
import CSP

initialState = State()
print ("initialState's possibleValues: ", initialState.possibleValues)
image = initialState.drawPossibleValues()
fig = plt.figure()
plt.imshow(image)
ax = fig.add_subplot(1, 1, 1)
ax.set_yticks(range(len(CSP.variables)))
ax.set_yticklabels(CSP.variables)
plt.show()

intermediateState = State(initialState.assignment, initialState.possibleValues,
                          "state1", "red")
print ("intermediateState's possibleValues: ", intermediateState.possibleValues)
image = intermediateState.drawPossibleValues()
fig = plt.figure()
plt.imshow(image)
ax = fig.add_subplot(1, 1, 1)
ax.set_yticks(range(len(CSP.variables)))
ax.set_yticklabels(CSP.variables)
plt.show()