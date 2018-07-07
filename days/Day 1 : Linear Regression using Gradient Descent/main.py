# necessary imports
import matplotlib.pyplot as plt
import pandas as pd
import code

# read csv
data = pd.read_csv('data.csv')

# extract from csv
x = list(data[data.columns[0]])
y = list(data[data.columns[1]])

# obtains best value of m and b for line
m,b =code.run()

# plot all the points of data using scatter plot
plt.scatter(x,y)

line = [m * i + b for i in x]
# plot the linear regression line
plt.plot(x,line)
plt.title("Linear Regression using gradient descent")    
plt.plot()
plt.savefig('figure.jpg')