import numpy as np
from beartype import beartype

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
        
@beartype
def eval_formula(formula: str)-> bool:
    operand_stack = []
    last = 0
    i = 0
    while i < len(formula):
        if formula[i].isdigit():
            operand_stack.append(int(formula[i]))            
        if formula[i] in "!":
            if len(operand_stack) < 1:
                break
            last1 = operand_stack[-1]
            operand_stack.pop()
            res = perform_operation(last1, 0, formula[i])
            operand_stack.append(res)
        elif formula[i] in "&|^>=":
            if len(operand_stack) <= 1:
                break
            last1 = operand_stack[-1]
            operand_stack.pop()
            last2 = operand_stack[-1]
            operand_stack.pop()
            res = perform_operation(last2, last1, formula[i])
            operand_stack.append(res)
        i += 1
    if len(operand_stack) > 0 and operand_stack[-1] == 1:
        last = True
    else: 
        last = False
    return last

def main():
   print(eval_formula("11|"))


if __name__ == "__main__":
    main()