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
    """
    This function implements the addition of two unsigned 32-bit integers using bitwise operations.

    Args:
        a (numpy.uint32): The first unsigned 32-bit integer.
        b (numpy.uint32): The second unsigned 32-bit integer.

    Returns:
        numpy.uint32: The sum of the two integers a and b.

    Explanation:
        This function uses an algorithm based on bitwise operations to perform addition.
        The general idea is to iterate through the bits of each integer, calculating carries and adding them
        correctly to obtain the final sum."""
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
def gray_code(n: np.uint32) -> np.uint32:
    """
    Converts a binary number to its corresponding Gray code.
    
    Args:
        n (numpy.uint32): The input binary number to be converted to Gray code.
    
    Returns:
        numpy.uint32: The Gray code equivalent of the input binary number."""
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