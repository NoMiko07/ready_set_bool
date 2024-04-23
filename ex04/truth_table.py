import numpy as np
from typing import List
from beartype import beartype
import numpy as np

def perform_operation(num1, num2, operator):
    """
    Performs a binary logical operation between two numbers based on the specified operator.

    Args:
        num1: The first number.
        num2: The second number.
        operator (str): The logical operation to perform ('!', '&', '|', '^', '>', '=').

    Returns:
        The result of the binary logical operation between the two numbers.
    """
    res = False
    if operator == "!":
        res = not num1
    elif operator == "&":
        res = num1 & num2
    elif operator == "|":
        res = num1 | num2
    elif operator == "^":
        res = num1 ^ num2
    elif operator == ">":
        res = not num1 or num2
    else:
        res = num1 == num2
    res = int(res)        
    return res

def fill_table(power: int, size: int)-> List[int]:
    """
     Fill the table with 0 or 1 depending on the power.
    
     Args:
         power (int): The number of consecutive 0s or 1s before switching.
         size (int): The size of the table.
    
     Returns:
         numpy.ndarray: The filled table with 0s and 1s.
 """
    table = np.zeros((size, 1))
    i = 0
    neg_or_pos = 0
    count_for_power = power
    while i < size:
        if neg_or_pos == 0:    
            table[i, 0] = 0
            count_for_power -= 1
        else:
            table[i, 0] = 1
            count_for_power -= 1
        if count_for_power == 0:
            count_for_power = power
            neg_or_pos = not neg_or_pos
        
        i+= 1
    return table.astype(int)

def number_of_variables(formula: str):
    i = 0
    variables_names = []
    for char in formula:
        if char.isalpha():
            i += 1
            variables_names.append(char)
    variables_names.append("=")
    return i, variables_names

def iterating_and_apply_perform_operation(matrix1, matrix2, operator):
    """
    iterating through the whole matrix and applying  the perform_operation function.
    Args:
        matrix1: The first matrix.
        matrix2: The second matrix.
        operator (str): The logical operation to perform ('!', '&', '|', '^', '>', '=').

    Returns:
        numpy.ndarray: The matrix after the application of the perform_operation function.
    """
    new_matrix = np.empty((matrix1.shape[0], 1))
    if operator == '!':
        for i in range(matrix1.shape[0]):
            new_matrix[i, 0] = perform_operation(matrix1[i, 0], 0, operator)
    else:
        for i in range(matrix1.shape[0]):
          new_matrix[i, 0] = perform_operation(matrix1[i, 0], matrix2[i, 0], operator)
    return new_matrix.astype(int)

    
def print_the_matrix(truth_table_matrix):
    for line in truth_table_matrix:
        print("|", end ='')
        for element in line:
            print(f" {element} |", end ="")
        print("")
    
    
@beartype
def print_truth_table(formula: str):
    nb_variables, variables_names = number_of_variables(formula)
    truth_table_matrix = np.zeros((pow(2, nb_variables), nb_variables) ,dtype=object)
    
    i = 0
    for j in range(len(formula)):
        if formula[j].isalpha():            
            truth_table_matrix[:, i] = fill_table(pow(2, nb_variables - (i + 1)), truth_table_matrix.shape[0]).flatten()
            i += 1
    stacked_truth_table = truth_table_matrix[:, :1]
    i = 1
    
    for j in range(len(formula)):
        if formula[j].isalpha() and j != 0:
            new_column =  fill_table(pow(2, nb_variables - (i + 1)), truth_table_matrix.shape[0]).flatten().reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
            i += 1
        elif formula[j] in "!":
            if stacked_truth_table.shape[1] < 1:
                raise ValueError("the string has no variables")   
            last_column = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = stacked_truth_table[:, :-1]
            new_column = iterating_and_apply_perform_operation(last_column, last_column, formula[j]) 
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
        elif formula[j] in "&|^>=":      
            if stacked_truth_table.shape[1] < 2:
                raise ValueError("not enough operand to perform the operator")
            last_column1 = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = stacked_truth_table[:, :-1]
            last_column2 = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            new_column = iterating_and_apply_perform_operation(last_column2, last_column1, formula[j])
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))

    last_column = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
    truth_table_matrix = np.hstack((truth_table_matrix, new_column))
    truth_table_matrix = np.vstack((variables_names, truth_table_matrix))
    print_the_matrix(truth_table_matrix)
    
def main():
   print_truth_table("AB&CE|")


if __name__ == "__main__":
    main()