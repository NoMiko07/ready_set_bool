from beartype import beartype

@beartype
class PowerSetGenerator:
    def __init__(self, set: list):
        self.set = set
        self.powerset = [[]]
    
    def generate(self)-> list: 
        for element in self.set:
            new_subset = [subset + [element] for subset in self.powerset]
            self.powerset.extend(new_subset)
        self.powerset.sort(key=lambda subset: (len(subset), subset))
        
        return self.powerset
    
    

    
@beartype
def powerset(set: list)-> list:
    A = PowerSetGenerator(set)
    B = A.generate()
    return B
    
def main():
    B = powerset([1, 2, 3])
    for sets in B:
        print (sets)


if __name__ == "__main__":
    main()