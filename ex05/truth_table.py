import numpy as np
from typing import List
from beartype import beartype
import numpy as np
import math 
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
    size_of_each_column = []
    first_line = truth_table_matrix[0]
    for element in first_line:
        size_of_each_column.append(int(len(element)))
    size_of_each_column_plustwo = [num + 2 for num in size_of_each_column]
    
    first_line_flag = True
    for line in truth_table_matrix:
        print("|", end ='')
        for i in range(len(line)):
            if first_line_flag == True:
                print("", line[i], "|", end ="")
            else:
                nb_of_left_space = int(size_of_each_column_plustwo[i] / 2)
                nb_of_right_space = int(size_of_each_column_plustwo[i] / 2)
                if size_of_each_column_plustwo[i] > 3:
                    if size_of_each_column_plustwo[i] % 2 == 0:
                        nb_of_right_space = int(size_of_each_column_plustwo[i] / 2) - 1
                    else :
                        nb_of_right_space = int(size_of_each_column_plustwo[i] / 2)
                print(" " * nb_of_left_space ,line[i], " " * nb_of_right_space, '|', sep='', end ="")
        print("")
        first_line_flag = False

def return_logical_connector(symbol: str)-> str:
    if symbol == "&":
        return "^"
    elif symbol == "|":
        return "v"
    elif symbol == "!":
        return "¬"
    elif symbol == "^":
        return "⊕"
    elif symbol == ">":
        return ">"
    elif symbol == "=":
        return "="
    return ""

def find_different_columns(arr1, arr2):
    dif_column = []
    if arr1.shape[0] != arr2.shape[0]:
        raise ValueError("Les deux tableaux doivent avoir le même nombre de lignes.")
    arr1_nb_col = arr1.shape[1]
    arr2_nb_col = arr2.shape[1]
    
    if arr1_nb_col >= arr2_nb_col:
        for col_idx in range(arr1.shape[1]):
            column = arr1[:, col_idx]
            first_letter = column[0]
            if first_letter not in arr2[0]:
                dif_column.append(column)
    else:       
        for col_idx in range(arr2.shape[1]):
            column = arr2[:, col_idx]
            first_letter = column[0]
            if first_letter not in arr1[0]:
                dif_column.append(column)
    dif_column = np.column_stack(dif_column)
    
    return dif_column

@beartype
def print_truth_table(formula: str):
    nb_variables, variables_names = number_of_variables(formula)
    truth_table_matrix = np.zeros((pow(2, nb_variables), nb_variables) ,dtype=object)
    
    i = 0
    for j in range(len(formula)):
        if formula[j].isalpha():            
            truth_table_matrix[:, i] = fill_table(pow(2, nb_variables - (i + 1)), truth_table_matrix.shape[0]).flatten()
            i += 1
    first_line = variables_names[0:1]
    stacked_truth_table = np.vstack((first_line, truth_table_matrix[:, :1]))
    fake_truth_table = stacked_truth_table
    i = 1
    for j in range(len(formula)):
        if formula[j].isalpha() and j != 0:
            stacked_first_line = stacked_truth_table[0]
            stacked_truth_table = stacked_truth_table[1:]
            new_column =  fill_table(pow(2, nb_variables - (i + 1)), truth_table_matrix.shape[0]).flatten().reshape(truth_table_matrix.shape[0], 1)
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
            i += 1
            stacked_first_line = np.hstack((stacked_first_line, formula[j]))
            stacked_truth_table = np.vstack((stacked_first_line, stacked_truth_table))
            
        elif formula[j] in "!":
            if stacked_truth_table.shape[1] < 1:
                raise ValueError("the string has no variables")
            name = stacked_truth_table[0:1, -1]
            last_column = stacked_truth_table[1:, -1].reshape(stacked_truth_table.shape[0] - 1, 1)
            stacked_truth_table = stacked_truth_table[:, :-1]
            stacked_first_line = stacked_truth_table[0]
            stacked_truth_table = stacked_truth_table[1:]
            new_column = iterating_and_apply_perform_operation(last_column, last_column, formula[j])
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
            fusion_name = return_logical_connector(formula[j]) + name
            stacked_first_line = np.hstack((stacked_first_line, fusion_name))
            stacked_truth_table = np.vstack((stacked_first_line, stacked_truth_table))
            last_column = stacked_truth_table[:, -1].reshape(stacked_truth_table.shape[0], 1)
            fake_truth_table = np.hstack((fake_truth_table, last_column))
            
        elif formula[j] in "&|^>=":      
            if stacked_truth_table.shape[1] < 2:
                raise ValueError("not enough operand to perform the operator")
            name1 = stacked_truth_table[0:1, -1]
            last_column1 = stacked_truth_table[1:, -1].reshape(stacked_truth_table.shape[0] - 1, 1)
            stacked_truth_table = stacked_truth_table[:, :-1]
            name2 = stacked_truth_table[0:1, -1]
            last_column2 = stacked_truth_table[1:, -1].reshape(stacked_truth_table.shape[0] - 1, 1)
            stacked_first_line = stacked_truth_table[0]
            stacked_truth_table = stacked_truth_table[1:]
            new_column = iterating_and_apply_perform_operation(last_column2, last_column1, formula[j])
            stacked_truth_table = np.hstack((stacked_truth_table, new_column))
            fusion_name = name1 + return_logical_connector(formula[j]) + name2
            stacked_first_line = np.hstack((stacked_first_line, fusion_name))
            stacked_truth_table = np.vstack((stacked_first_line, stacked_truth_table))
            last_column = stacked_truth_table[:, -1].reshape(stacked_truth_table.shape[0], 1)
            fake_truth_table = np.hstack((fake_truth_table, last_column))
        
    truth_table_matrix = np.vstack(( variables_names[0:-1], truth_table_matrix))
    diff_column = find_different_columns(fake_truth_table, truth_table_matrix)
    truth_table_matrix = np.hstack((truth_table_matrix, diff_column))
    print_the_matrix(truth_table_matrix)
    
def main():
   print_truth_table("A!B!&C!&")


if __name__ == "__main__":
    main()