from BoolBinaryTree import BoolBinaryTree, negation_normal_form
from truth_table import *

def main():
    NNF = negation_normal_form('AB|!')
    print(NNF)
    print_truth_table(NNF)

if __name__ == "__main__":
    main()