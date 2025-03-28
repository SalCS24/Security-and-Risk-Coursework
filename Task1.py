# -- START OF YOUR CODERUNNER SUBMISSION CODE
# INCLUDE ALL YOUR IMPORTS HERE

from dhCheck_Task1 import dhCheckCorrectness

import numpy as np
from math import sqrt

# Method which aims to calculate the probability (prob1) is in between the upper bound and lower bound
# lower bound = a
# upper bound = b
# mode = c
# point1 = chosen point between uper and blower bounds



# Use cumulative distribution function, which is a subset of the Triangular Distribution 
# The function is used to identify the probability that point 1 is above or equal to the lower bound, or lower or equal to upper bound
# CDF is used to identify probability, which is why it is used here.
def Triangular_Distribution_Calc(a, b, c, point1):
    if point1 < a:
        return 0 
    elif point1 > b:
        return 1
    elif a <= point1 < c:
        prob1 =((point1 - a)**2) / ((b-a) * (c-a))
    elif c < point1 <= b:
        prob1 = 1 - ((b - point1)**2) / ((b -a) * (b-c))
    return prob1

# Calculate the mean of the 3 values, given you the average.
# Which gives us the mean 
def triangular_Mean(a, b, c):
    MEAN_t = (a + b + c)/3
    return MEAN_t

# The output is utilised as the AV value when calculating the ALE
def triangular_Median(a, b, c):
    conditional = (a + b) /2
    if c >= conditional:
        median = a + sqrt((b-a)*(c-a)/2)
    else:
        median = b - sqrt((b-a)*(b-c)/2)
    MEDIAN_t = median
    return MEDIAN_t

def occurence_Median(number_set, prob_set):
    # for loop whih iteratese through the length of number_set
    # calculating the value of each element's risk value based of the occurence multiplied by the probability
    total_Risks = 0
    prob_Sum = sum(prob_set)
    for i in range(len(number_set)):
        total_Risks += number_set[i] * prob_set[i]
   
    # calculate the risk values
    

    mean_Risks = total_Risks / prob_Sum

    return mean_Risks
    
def occurence_Variation(number_set, prob_set):
    #Instantiate total_risks and squared sum to avoid having an error within the for loop
    total_Risks = 0
    squaredSum = 0
    for i in range(len(number_set)):
        individual_Risks = number_set[i] * prob_set[i]
        total_Risks += individual_Risks
        squaredSum += (number_set[i] **2) * prob_set[i]
        
    individual_Variation = squaredSum - (total_Risks **2)
    return individual_Variation

def log_Distribution(mu, sigma, num):
    # num is the number of samples we wish to generate
    log_Samples = np.random.lognormal(mu, sigma, num)
    return log_Samples
    
def pareto_Distribution(xm, alpha, num):
    pareto_Samples = np.random.pareto(alpha, num) * xm
    return pareto_Samples

def monte_Carlo(num, point2, mu, sigma, xm, alpha, point3, point4):
    # creates an array of length num which holds a all the distributions based on lognormal distributions
    log_Samples = log_Distribution(mu, sigma, num)
    # creates an array of length num which holds all the distributions based on pareto distribution
    pareto_Samples = pareto_Distribution(xm, alpha, num)

    # calculates the total impact of the samples
    total_Impact = log_Samples + pareto_Samples

    # find the total number of impact points which are larger than point 2
    Desired_Impact = total_Impact > point2
    
    # checks if the values are higher than point 2 if they are then increment the truths variable
    truths = sum(Desired_Impact)
    # calculate the probability by dividing the number of larger points over the total amount of points
    prob2 = truths/len(Desired_Impact)

    # check if the total impact is < point4 and > pcoint3
    second_Impact = (total_Impact > point3) & ( total_Impact < point4)

    secondary_Truths = sum(second_Impact)
    prob3 = secondary_Truths/len(second_Impact)
    
    return prob2, prob3
# Task 1 is a series of calculations which aim to retrieve the Annualise Loss Expectancy (ALE)
#KEY RESOURCES:
# https://en.wikipedia.org/wiki/Annualized_loss_expectancy
# https://en.wikipedia.org/wiki/Single-loss_expectancy
# https://en.wikipedia.org/wiki/Triangular_distribution
# https://en.wikipedia.org/wiki/Log-normal_distribution
# https://en.wikipedia.org/wiki/Pareto_distribution
# https://en.wikipedia.org/wiki/Monte_Carlo_method
def Task1(a, b, c, point1, number_set, prob_set, num, point2,
mu, sigma, xm, alpha, point3, point4):

    prob1 = Triangular_Distribution_Calc(a , b, c, point1)

    MEAN_t = triangular_Mean(a, b, c)
    # Median_t is the value which will be used as AV, in the ALE calculation
    MEDIAN_t = triangular_Median(a, b, c)
    # Mean_d is the value which will be used as ARO
    MEAN_d = occurence_Median(number_set, prob_set)
    VARIANCE_d = occurence_Variation(number_set, prob_set)
    prob2, prob3 = monte_Carlo(num, point2, mu, sigma, xm, alpha, point3, point4)
    EF = prob2
    #ALE = ARO x SLE
    #SLE = AV x EF
    SLE = MEDIAN_t * EF
    ALE = MEAN_d * SLE

    return (prob1, MEAN_t, MEDIAN_t, MEAN_d, VARIANCE_d, prob2, prob3, ALE)
