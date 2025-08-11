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
    return np.uint32(a)
    
def get_last_bit(num):
    # Use a binary mask to extract the last bit
    last_bit = num & 1
    return last_bit

@beartype
def multiplier(a: np.uint32, b: np.uint32) -> np.uint32:
    result = np.uint32(0)
    ia = a
    while ia > 0:
        result = adder(result, b)
        ia -= 1
    return result

def main():
    a = np.uint32(21)
    b = np.uint32(2)
    print(multiplier(a ,b))


if __name__ == "__main__":
    main()