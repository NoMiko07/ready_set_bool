from __future__ import annotations
from beartype import beartype

@beartype
class BoolBinaryBranch:
    def __init__(self,
                 data: str,
                 left: BoolBinaryBranch = None,
                 right: BoolBinaryBranch = None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        left_str = str(self.left) if self.left else ""
        right_str = str(self.right) if self.right else ""
        if self.left or self.right:
            return f"{left_str}{right_str}{self.data}"
        return self.data
    
    def negation_normal_form_branch(self):
        if self.data == '>':
            new_left = BoolBinaryBranch("!",  self.left)
            self.left = new_left
            self.data = "|"
        elif self.data == "^":
            new_left = BoolBinaryBranch('&', self.left, BoolBinaryBranch('!', self.right))
            new_right = BoolBinaryBranch('&',BoolBinaryBranch('!', self.left) , self.right)
            self.data = "|"
            self.left = new_left
            self.right = new_right
        elif self.data == "=":
            new_left = BoolBinaryBranch('&', self.left, self.right)
            new_right = BoolBinaryBranch('&', BoolBinaryBranch('!', self.left), BoolBinaryBranch('!', self.right))
            self.data = "|"
            self.left = new_left
            self.right = new_right
        elif self.data == '!' and not self.left.data.isupper():
            self.left.negation_normal_form_branch()
            new_left = BoolBinaryBranch("!", self.left.left)
            new_right = BoolBinaryBranch("!", self.left.right)           
            self.data = '&' if self.left.data == '|' else '|'    
            self.left = new_left
            self.right = new_right
        if self.left:
            while self.left.data == '!' and self.left.left.data == '!':
                self.left = self.left.left.left
            self.left.negation_normal_form_branch()
        if self.right:
            while self.right.data == '!' and self.right.left.data == '!':
                self.right = self.right.left.left
            self.right.negation_normal_form_branch()
    
    def is_minimal_form(self)-> bool:
        return self.data.isalpha() or self.data == '!'
    
    def is_cnf(self, is_conjunctive: bool)-> bool:
        if self.is_minimal_form():
            return True
        if is_conjunctive and self.data == '&':
            return False
        if self.left.is_minimal_form() and self.right.is_minimal_form():
            return True
        if self.data != '&':
            is_conjunctive = True
        return self.left.is_cnf(is_conjunctive) and self.right.is_cnf(is_conjunctive)
    
    def apply_cnf_distributivity(self)-> None:
        if self.is_minimal_form():
            return
        if self.data == "|":
            target: BoolBinaryBranch = None
            opposite: BoolBinaryBranch = None
            if self.right.data == "&":
                target = self.right
                opposite = self.left
            elif self.left.data == "&": 
                target = self.left
                opposite = self.right
            if target:
                self.left = BoolBinaryBranch('|', target.left, opposite)
                self.right = BoolBinaryBranch('|', target.right, opposite)
                self.data = '&'
        self.left.apply_cnf_distributivity()
        self.right.apply_cnf_distributivity()
        
    def find_not_conjuctive_set(self):
        result = []
        result += (self.left.find_not_conjuctive_set() if self.left.data == '&' else [self.left]) 
        result += (self.right.find_not_conjuctive_set() if self.right.data == '&' else [self.right])
        return result
    
    def find_not_or_set(self):
        result = []
        result += (self.left.find_not_or_set() if self.left.data == '|' else [self.left])
        result += (self.right.find_not_or_set() if self.right.data == '|' else [self.right])
        return result
    
    def change_or_logical(self):
        if self.data == "&":
            self.sort_or_logical()
        elif self.data == "|":
            result = self.find_not_or_set()
            self.left = result[0]
            self.right = result[1]
            
            if len(result) > 2:
                target = self
                for i in range(2, len(result)):
                    target.right = BoolBinaryBranch('|', result[i - 1], result[i])
                    target = target.right
            
    
    def sort_or_logical(self):
        if self.is_minimal_form():
            return
        if self.data == '|':
            self.change_or_logical()
        self.left.change_or_logical()
        self.right.change_or_logical()
        

    
@beartype
class BoolBinaryTree:
    def __init__(self, formula: str):
        branches = []
        for i in formula:
            if i.isalpha():
                branches.append(BoolBinaryBranch(i))
            elif i == '!':
                if len(branches) < 1:
                    raise ValueError("Not enough operands")
                root = branches.pop()
                branches.append(BoolBinaryBranch(i, root))
            elif i in '&=>^|':
                if len(branches) < 2:
                    raise ValueError("Not enough operands")
                right = branches.pop()
                left = branches.pop()
                branches.append(BoolBinaryBranch(i, left, right))
        self.root = branches[0]        

    def __str__(self) -> str:
        return str(self.root)
    
    def NNF(self):
        while self.root.data == '!' and self.root.left.data == '!':
            self.root = self.root.left.left
        self.root.negation_normal_form_branch()
    
    def conjuctive_normalize(self):
        while not self.root.is_cnf(False):
            self.root.apply_cnf_distributivity()

        self.root.sort_or_logical()

        if self.root.is_minimal_form() or self.root.data != "&":
            return

        result = self.root.find_not_conjuctive_set()
        new_root = BoolBinaryBranch("&", result[0], result[1])
        if len(result) > 2:
            target = new_root
            for i in range(2, len(result)):
                target.right = BoolBinaryBranch('&', result[i - 1], result[i])
                target = target.right

        self.root = new_root
    
    
    def CNN(self):
        self.NNF()
        self.conjuctive_normalize()
        return self.root
        
    
@beartype     
def conjunctive_normal_form(formula: str)-> str:
    test = BoolBinaryTree(formula)
    test.CNN()
    return str(test)
  

def main():
    CNF = conjunctive_normal_form('AB|!C!&')
    print(CNF)


if __name__ == "__main__":
    main()