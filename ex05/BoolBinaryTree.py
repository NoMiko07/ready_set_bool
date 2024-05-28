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
    
  
@beartype  
def negation_normal_form(formula: str)-> str:
    test = BoolBinaryTree(formula)
    test.NNF()
    return str(test)
    
def main():
    NNF = negation_normal_form("AB|!A&")
    print(NNF)


if __name__ == "__main__":
    main()