# Import the necessary libraries
from numpy import * 

# It returns average error for the b and m parameters
def compute_error_for_given_points(b, m, points):
    totalError = 0
    # Iterate for length of points times
    for i in range(0,len(points)):
        x = points[i,0]
        y = points[i,1]
        totalError += (y-(m*x+b))**2
    return totalError/float(len(points))


# Find gradient for each value
def step_gradient(b_current, m_current, points, learningRate):
    # gradient descent
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0,len(points)):
        # obtain value of x and y
        x = points[i,0]
        y = points[i,1]

        #calcualte b_gradient
        b_gradient += -(2/N) * (y-((m_current*x) + b_current))

        #calcualte m_gradient
        m_gradient += -(2/N) *x* (y-((m_current*x) + b_current))

    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]


# It returns the optimal value for b and m
def gradient_descent_runner(points,starting_b,starting_m,learning_rate,num_iteration):
    # intialize the values
    b = starting_b
    m = starting_m

    # Iterate for num_iteration times
    for i in range(num_iteration):
        b,m = step_gradient(b,m,array(points),learning_rate)
    return [b,m]


def run():
    points = genfromtxt('data.csv',delimiter=",")
    # hyper parameter
    learning_rate = 0.0001
    #y = mx+b (slope formula)
    initial_b = 0
    initial_m = 0
    num_iteration = 1000
    [b,m] = gradient_descent_runner(points,initial_b,initial_m, learning_rate, num_iteration)
    error = compute_error_for_given_points(b,m,points)
    print("After {} iterations\nb = {}\nm = {}\nerror = {}".format(num_iteration,b,m,error))
    return [m,b]