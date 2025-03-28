# -- START OF YOUR CODERUNNER SUBMISSION CODE
# INCLUDE ALL YOUR IMPORTS HERE

from dhCheck_Task3 import dhCheckCorrectness

import numpy as np
from scipy.optimize import linprog

def Task3(x, y, z, x_initial, c, x_bound, se_bound, ml_bound):
 # TODO
 weights_b = calculate_Weights_B(x,y)
 weights_d = calculate_Weights_D(x,z)
 x_add = safeGuard_Enhancement(x,y, z, x_initial, c, x_bound, se_bound, ml_bound)
 return (weights_b, weights_d, x_add)

# Method which is in charge of calculating weightb (b0, b1, b2, b3, b4)
# Finding these coefficients allows us to find the effect of each security control


def calculate_Weights_B(x, y):
 # create arrays for the data
 x_Array = np.array(x)
 y_Array = np.array(y)
 # Transpose the x_Array from (4,9) to (9,4)
 x_Array =  x_Array.T
 # Create an array of ones to act as the intercept or b0
 ones_Array = np.ones((x_Array.shape[0],1))
 # Add the ones array as a column to the x_Array
 new_X = np.hstack((ones_Array, x_Array))
  
 # calculate weights_b using linalg
 # coefficient equation d = (XT * X)^-1 * XT * y
 XTX = new_X.T @ new_X
 XTY = new_X.T @ y
 weights_b = np.linalg.inv(XTX) @ XTY
 
 return weights_b

# Method which is in charge of calculating weightb (d0, d1, d2, d3, d4)
def calculate_Weights_D(x, z):
 # create an array to hold the datasets
 x_Array = np.array(x) #X_array dimensions = (4, 9)
 z_Array = np.array(z)
 x_Array = x_Array.T # new dimensions = (9, 4)
  # Create an array of ones to act as the intercept or b0
 ones_Array = np.ones((x_Array.shape[0],1))
 # Add the ones array as a column to the x_Array
 new_X = np.hstack((ones_Array, x_Array))
 # calculate weights_b using linalg
 # coefficient equation d = (XT * X)^-1 * XT * y
 XTX = new_X.T @ new_X
 XTZ = new_X.T @ z
 weights_d = np.linalg.inv(XTX) @ XTZ
 
 return weights_d
# method which aims to enhance the security protocols 
# ensuring that meet certain guidelines
# x_initial : current number of each type of security control in use
# c : list of costs associated with adding one unit of each type of control
# x_bound : the limits in which the x_bound can go to
# se_bound :the minimum acceptable safeguard effect
# ml_bound : upper limit of the maintenance load
# x_add: the additional security controls for each type of x 
def safeGuard_Enhancement(x,y, z, x_initial, c, x_bound, se_bound, ml_bound):
    # Create the np arrays for the parameters
    x_initial = np.array(x_initial)
    costs_Array = np.array(c)
    x_bound = np.array(x_bound)
    
    # compute the coefficients 
    weights_b = calculate_Weights_B(x, y)
    weights_d = calculate_Weights_D(x, z)
    
     # Extract values
    b0, b1, b2, b3, b4 = weights_b
    d0, d1, d2, d3, d4 = weights_d
    
    # Calculate the intiial safeguard effect of the system
    Current_Safeguard_Effect_Array = b0 + b1 * x_initial[0] + b2 * x_initial[1] + b3 * x_initial[2] + b4 * x_initial[3]
    
    #Calculate  the amount of safeguard_effect required to achieve the minimum
    safeGuard_Diff = se_bound - Current_Safeguard_Effect_Array
    
    # Calculate the initial maintenance load of the system
    Current_Maintenance_Load_Array = d0 + d1 * x_initial[0] + d2 * x_initial[1] + d3 * x_initial[2] + d4 * x_initial[3]
    # Calculate the diff in the maintenance load
    ML_Diff = ml_bound - Current_Maintenance_Load_Array
    # Create an array to hold the coefficients of the safeguard effect and maintenance load
    A_ub = [[-b1, -b2, -b3, -b4], [d1, d2, d3, d4]]
    # Create an array to hold the constraints which will be used in conjunction with the coefficient
    B_ub = [-safeGuard_Diff, ML_Diff]
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    # create an empty list for bounds
    bounds = []
    for i in range(len(x_initial)):
        lower_bound = 0
        upper_bound = x_bound[i] - x_initial[i]
        bounds.append((lower_bound, upper_bound))
    # use linprog and utilise the variables created earlier into them
    optimisation = linprog(costs_Array, A_ub=A_ub, b_ub=B_ub, bounds=bounds, method="highs")
    # Check if the linprogramming function returns a success, if so pass it to x_add
    if optimisation.success:
        x_add = optimisation.x
    else: 
        print("Linear programming has failed")
    return x_add
# -- END OF YOUR CODERUNNER SUBMISSION CODE
