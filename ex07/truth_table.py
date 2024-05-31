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
    
    num1 = int(num1)
    num2 = int(num2)
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


def number_of_variables(formula: str):
    variables_name: list[str] = []
    
    for j in range(len(formula)):
        if formula[j] not in formula[:j] and formula[j].isalpha():
            variables_name += formula[j]
    
    return len(variables_name), variables_name


def fill_table_for_variables(formula: str)-> np.ndarray:
    nb_variables, variables_name = number_of_variables(formula)
    basic_truth_table = np.zeros((pow(2, nb_variables), nb_variables) ,dtype=object)
    
    i = 0
    for j in range(len(formula)):
        if formula[j] not in formula[:j] and formula[j].isalpha():
            basic_truth_table[:, i] = fill_table(pow(2, nb_variables - (i + 1)), basic_truth_table.shape[0]).flatten()
            i += 1
    variables_name_array = np.array(variables_name).reshape(1, -1)
    basic_truth_table = np.vstack((variables_name_array, basic_truth_table))
    
    basic_truth_table = fill_table_for_variablesNOT(formula, basic_truth_table)
    return basic_truth_table
    

def return_the_variable_column(basic_truth_table: np.ndarray, which_column: str)-> np.ndarray:
    first_line = basic_truth_table[0:1]
    first_line = first_line.reshape(first_line.shape[1], first_line.shape[0])
    i = 0
    for column in first_line:
        if column == which_column:
            break
        i+= 1

    variable_column = basic_truth_table[1:, i:i + 1]
    return variable_column

def check_double_occurence_variable(first_line: np.ndarray, to_check: str)-> bool:
    if to_check in first_line:
        return True    
    return False

def fill_table_for_variablesNOT(formula: str, basic_truth_table: np.ndarray)-> np.ndarray:   
    for j in range(len(formula)):
        if formula[j] == '!':
            which_column = formula[j - 1]
            new_column_name = which_column + "!"
            if check_double_occurence_variable(basic_truth_table[0:1], new_column_name):
                continue
            new_column = return_the_variable_column(basic_truth_table, which_column)
            new_column = iterating_and_apply_perform_operation(new_column, new_column, "!")
            new_column = np.vstack((new_column_name, new_column))
            basic_truth_table = np.hstack((basic_truth_table, new_column))
    return basic_truth_table  
    

@beartype
def return_truth_table(formula: str):
    truth_table = fill_table_for_variables(formula)
    variable_list: list = []
    
    for j in range(len(formula)):
        if formula[j].isalpha():
            variable_name = formula[j]
            if j + 1 < len(formula) and formula[j + 1] == "!":
                variable_name = formula[j] + "!"
            variable_list.append(variable_name)
        elif formula[j] in "&|^>=":
            if len(variable_list) < 2:
                raise ValueError(f"not enough operand to perform the operator {formula[j]}")
            second_operand = variable_list.pop()
            first_operand = variable_list.pop()
            
            second_column = return_the_variable_column(truth_table, second_operand)
            first_column = return_the_variable_column(truth_table, first_operand)
            new_column = iterating_and_apply_perform_operation(first_column, second_column, formula[j])
            new_column = np.vstack(('=', new_column))
            variable_list.append("=")
            if check_double_occurence_variable(truth_table[0:1], "="):
                truth_table = truth_table[:, :-1]
            truth_table = np.hstack((truth_table, new_column))
    return truth_table[1:, -1]
    
@beartype
def sat(formula: str)-> bool:
    result_column = return_truth_table(formula)
    
    for result in result_column:
        if int(result) > 0:
            return True
        
    return False

def main():
   print(sat("AB|C&&"))
   

if __name__ == "__main__":
    main()