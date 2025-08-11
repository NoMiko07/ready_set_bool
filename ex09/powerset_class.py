from beartype import beartype

@beartype
class SetEvaluation:
    def __init__(self, formula: str, sets: list):
        self.formula = formula
        self.sets = sets
        self.result = []
        self.universe = []
    
    def parsing_errors(self):
        alpha_sets = 0
        operator = 0
        for element in self.formula:
            if element.isupper():
                alpha_sets += 1
            else:
                operator += 1
        if operator > alpha_sets:
            raise ValueError("Formula or sets is invalid")
        
        for subsets in self.sets:
            for element in subsets:
                if not isinstance(element, int):
                    raise ValueError("set or subsets must contain only integers")
    


    def perform_union(self, set1, set2)-> list:
        newset = []
        newset.extend(set1)
        newset.extend(set2)
        newset = list(set(newset))
        newset.sort()
        
        return newset
    
    def define_universe(self)-> list:
        first_set = []
        alpha_sets = 0
        for element in self.formula:
            if element.isupper():
                alpha_sets += 1
        set_numbers = len(self.sets)
        if set_numbers > alpha_sets:
            sets_cpy = self.sets.copy()
            first_set = sets_cpy.pop()
            if len(sets_cpy) > 1:
                first_set = sets_cpy.pop()
                while len(sets_cpy) > 0:
                    set2 = sets_cpy.pop()
                    first_set = self.perform_union(first_set, set2)

        return first_set
         
    def perform_intersection(self, set1:list, set2: list)-> list:        
        intersection_result = [item for item in set1 if item in set2]
        intersection_result.sort()
        
        return intersection_result
    
    
    def perform_symmetric_difference(self, union:list, intersection: list)-> list:
        s_d_result = [item for item in union if item not in intersection]    
        
        return s_d_result
    
    def perform_operation(self, set1: list, set2: list, operation: str)-> list:
        result = []
        if operation == "|":
            result = self.perform_union(set1, set2)
        elif operation == "&":
            result = self.perform_intersection(set1, set2)
        elif operation == "^":
            union = self.perform_union(set1, set2)
            intersection = self.perform_intersection(set1, set2)
            result = self.perform_symmetric_difference(union, intersection)
        elif operation == ">":
            result = self.perform_symmetric_difference(self.universe, set1)
            result = self.perform_union(result, set2)
        elif operation == "=":
            diff1 = self.perform_symmetric_difference(self.universe, set1)
            diff2 = self.perform_symmetric_difference(self.universe, set2)
            union_diff = self.perform_intersection(diff1, diff2)
            inter = self.perform_intersection(set1, set2)
            result = self.perform_union(union_diff, inter)
        return result

    
    def generate_result(self): 
        self.parsing_errors()
        self.universe = self.define_universe()
        for element in self.formula:
            if element.isupper():
                self.result.append(self.sets.pop(0))
            elif element == '!':
                set1 = self.result.pop()
                self.result.append(self.perform_symmetric_difference(self.universe, set1))
            else:
                if len(self.result) < 2:
                    raise ValueError("Not enough sets to perform the operation")
                set2 = self.result.pop()
                set1 = self.result.pop()
                self.result.append(self.perform_operation(set1, set2, element))
        
        print(self.result)
    
    

    
@beartype
def eval_set(formula: str, sets: list)-> list:
    A = SetEvaluation(formula, sets)
    A.generate_result()
    return []
    
def main():    
    sets = [[0, 1, 2],
            [2, 3, 4, 5],
            ]
    
    eval_set("AB>", sets)


if __name__ == "__main__":
    main()