# -- START OF YOUR CODERUNNER SUBMISSION CODE
# INCLUDE ALL YOUR IMPORTS HERE

import numpy as np
from dhCheck_Task2 import dhCheckCorrectness
def Task2(num, table, probs):
 prob1 = probability1(table)
 prob2 = probability2(table)
 prob3 = probability3(num, table, probs)
 return (prob1, prob2, prob3)

# Calculate the probability that 3 <= x <= 4
# Add up the cells which fall within the column of x = 3 or x = 4
# then divide by the total number of occurence within the table

def probability1(table):
 # Add up all occurences within the table
 totalValue = np.sum(table)
 col2_0 = table[0][1]
 col2_1 = table[1][1]
 col2_2 = table[2][1]
 col3_0 = table[0][2]
 col3_1 = table[1][2]
 col3_2 = table[2][2]
 Values = col2_0 + col2_2 + col2_1 + col3_0 + col3_1 + col3_2

 prob1 = Values / totalValue 
 return prob1

# calculate the probability that  x + y are less or equal to 10
# Add up all cells which have an x and y value which is equivalent to 10.
# Then divide by the total number of occurences within the table
def probability2(table):
 # Add up all occurrences within the table
 totalValue = np.sum(table)

 col1_0 = table[0][0]
 col1_1 = table[1][0]
 col1_2 = table[2][0]
 col2_0 = table[0][1]
 col2_1 = table[1][1]
 col3_0 = table[0][2]
 
 Values =  col1_0 +  col1_1 +  col1_2 +  col2_0 +  col2_1 +  col3_0
 
 prob2 = Values / totalValue
 return prob2
# Bayes theorem: P(A|B) = P(B|A) * P(A) / P(B)
# P(A|B) = probability of A given that B is true
# P(B|A) = probability of B given that A is true 
# This method aims to calulcate the probabiltiy that Y = 8 and that a test is positive
# P(Y = 8|T) = P(T|Y=8) * P(Y = 8) / P(T)
# P(T| Y = 8) probability of a positive test while Y = 8
# P(T) are all occurence where the test is positive
# An issue face when calculting the P(T)
# Trying To calculate P(T) directly using the bottom row
# PX2 holds the probs for the whole column therefore isolating a single row doesnt return the correct answer.
def probability3 (num, table, probs):
   # extract the conditional probabilities from the probs array
   PX2, PX3, PX4, PX5, PY6, PY7 = probs
   # extract all cells from the 2d array table
   a, b, c, d = table[0]
   e, f, g ,h = table[1]
   i, j, k, l = table[2]


   # Calculate the sum of all rows
   Row_6 = a + b + c + d
   Row_7 = e + f + g + h
   Row_8 = i + j + k + l
  
   # Calculate the sums of all columns
   Column_2 = a + e + i
   Column_3 = b + f + j
   Column_4 = c + g + k
   Column_5 = d + h + l
   # calculate P(Y=8)find all cells which correspond to Y = 8
   # Take the values within that range and normalise by dividing by num
   py_8 = Row_8 / num

   # calculate P(T | Y = 8)
   # Find the positive test when Y = 8
   # Find all values present when Y = 8 (final row)
   # Find the probability of an occurence being tested positive in the table
   # accomplished by multiplying PX values by the columns
   # Subtract the first 2 rows by multiplying the probabilities of Rows 6 and 7
   table_test_positive = (Column_2 * PX2) + (Column_3 * PX3) + (Column_4 * PX4) + (Column_5 * PX5)
   
   eliminate_top_two_Rows = ((Row_6 * PY6) + (Row_7 * PY7))

   p_t = table_test_positive - eliminate_top_two_Rows

   # divide the extracted probability by the number of occurences in the final rows
   p_t_given_Y8 = p_t/ Row_8
   

   # calculate P(T)
   # To calculate the probability that an occurence returns a positive test
   Ptx = table_test_positive / num
   # Use Bayes theorem to find the P(Y = 8 | T)
   p_y_given_T = (p_t_given_Y8 * py_8) / Ptx

   prob3 = p_y_given_T
   return prob3
