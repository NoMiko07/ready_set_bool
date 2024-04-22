import numpy as np
from beartype import beartype

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
    return a


def main():
    a = np.uint32(32)
    b = np.uint32(10)
    print(adder(a ,b))


if __name__ == "__main__":
    main()