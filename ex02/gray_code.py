import numpy as np
from typing import List
from beartype import beartype


def convert_to_binary_array(num: np.uint32) -> List[int]:
    binary_array = []
    while num != 0:
        binary_array.append(num & 1)
        num = num >> 1
        
    binary_array.reverse()
    return binary_array

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

@beartype
def gray_code(n: np.uint32) -> np.uint32:
    binary_array = convert_to_binary_array(n)
    gray = 0
    i = 0
    
    while i < len(binary_array):
        if i == 0:
           gray = binary_array[i] << len(binary_array) - 1
        else:
            dif = binary_array[i] ^ binary_array[i - 1]
            dif = dif << len(binary_array) - (i + 1)
            gray = adder(np.uint32(gray), np.uint32(dif))
        i += 1
    
    return np.uint32(gray)

def main():
    a = np.uint32(7)
    print(gray_code(a))


if __name__ == "__main__":
    main()