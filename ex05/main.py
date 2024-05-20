from BoolBinaryTree import BoolBinaryTree
from truth_table import *

def main():
    test = BoolBinaryTree("AB|!C&")
    test.negation_normal_form()
    test_str = str(test)
    print_truth_table(test_str)

if __name__ == "__main__":
    main()