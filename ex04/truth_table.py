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
    return i, variables_names

def iterating_and_apply_perform_operation(matrix1, matrix2, operator):
    new_matrix = np.empty((matrix1.shape[0], 1))
    if operator == '!':
        for i in range(matrix1.shape[0]):
            new_matrix[i, 0] = perform_operation(matrix1[i, 0], 0, operator)
    else:
        for i in range(matrix1.shape[0]):
          new_matrix[i, 0] = perform_operation(matrix1[i, 0], matrix2[i, 0], operator)
    return new_matrix.astype(int)
    
@beartype
def print_truth_table(formula: str):
    nb_variables, variables_names = number_of_variables(formula)
    truth_table_matrix = np.zeros((pow(2, nb_variables), nb_variables) ,dtype=object)
    
    for j in range(len(formula)):
        if formula[j].isalpha():            
            truth_table_matrix[:, j] = fill_table(pow(2, nb_variables - (j + 1)), truth_table_matrix.shape[0]).flatten()
    matrix_without_last_column = truth_table_matrix[:, :-1]
    matrixt_last_column = truth_table_matrix[:, -1].reshape(truth_table_matrix.shape[0], 1)
    stacked_truth_table = truth_table_matrix[:, :1]
    
    for j in range(len(formula)):
        if formula[j].isalpha() and j != 0:
            new_column =  fill_table(pow(2, nb_variables - (j + 1)), truth_table_matrix.shape[0]).flatten().reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
        elif formula[j] in "!":
            if stacked_truth_table.shape[1] < 1:
                raise ValueError("the string has no variables")   
                
            #this is sus
            last_column = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            res_column = iterating_and_apply_perform_operation(last_column, last_column, formula[j])
        elif formula[j] in "&|^>=":      
            if stacked_truth_table.shape[1] < 2:
                raise ValueError("not enough operand to perform the operator")
            last_column1 = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = stacked_truth_table[:, :-1]
            last_column2 = stacked_truth_table[:, -1].reshape(truth_table_matrix.shape[0], 1)
            res_column = iterating_and_apply_perform_operation(last_column2, last_column1, formula[j])
            print("last\n",last_column1,"\nlast2\n", last_column2, "\nres\n", res_column)
            print("test\n", stacked_truth_table)
            
    print(stacked_truth_table)
    
def main():
   print_truth_table("ABC&")


if __name__ == "__main__":
    main()