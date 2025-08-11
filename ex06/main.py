from BoolBinaryTree import BoolBinaryTree, conjunctive_normal_form
from truth_table import *

def main():
    CNF = conjunctive_normal_form('AB&C&D&')
    print(CNF)
    print_truth_table(CNF)

if __name__ == "__main__":
    main()