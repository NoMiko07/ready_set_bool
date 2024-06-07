from __future__ import annotations
from beartype import beartype

@beartype
class PowerSetGenerator:
    def __init__(self, set: list):
        self.set = set
        self.powerset = [[]]
        
        
    def __str__(self):
        return self.set
    
    def generate(self)-> list: 
        for element in self.set:
            new_subset = [subset + [element] for subset in self.powerset]
            self.powerset.extend(new_subset)
        self.powerset.sort(key=lambda subset: (len(subset), subset))
        
        return self.powerset
    
    

    
@beartype
def powerset(set: list):
    A = PowerSetGenerator(set)
    B = A.generate()
    print(B)
    return None
    
def main():
    powerset([1, 2, 3])


if __name__ == "__main__":
    main()