import numpy as np
from beartype import beartype

@beartype
def adder(a: np.uint32, b: np.uint32) -> np.uint32:
    
    i = 32    
    
    while i > 0:
        hold = a & b
        a = a ^ b
        if hold == 0:
            break
        b = hold << 1
        i -= 1        
    return a


def main():
    a = np.uint32(0)
    b = np.uint32(0)
    print(adder(a ,b))


if __name__ == "__main__":
    main()