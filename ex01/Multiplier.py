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
    return np.uint32(a)
    
def get_last_bit(num):
    # Use a binary mask to extract the last bit
    last_bit = num & 1
    return last_bit

@beartype
def multiplier(a: np.uint32, b: np.uint32) -> np.uint32:
    """
     This function multiplies two unsigned 32-bit integers using bitwise operations.
    
     Args:
         a (numpy.uint32): The first unsigned 32-bit integer.
         b (numpy.uint32): The second unsigned 32-bit integer.
    
     Returns:
         numpy.uint32: The product of the two integers a and b.
    
     Explanation:
         This function implements multiplication using bitwise operations.
         It iterates through the bits of the second integer (b) and, for each bit,
         calculates the product of the first integer (a) with the bit of b.
         The results are accumulated to obtain the final product."""
    ib = 0
    final_res = 0
    while b != 0:        
        last_bit_b = get_last_bit(b)
        binary_power = 0
        ia = 0
        binary_product_a = 0
        temp_a = a
        while temp_a != 0:
            last_bit_a = get_last_bit(temp_a)
            binary_power = last_bit_a & last_bit_b
            if ia != 0:
                binary_power = binary_power << ia
            binary_product_a = adder(np.uint32(binary_product_a), np.uint32(binary_power))
            temp_a = temp_a >> 1
            ia += 1
        
        res_b = binary_product_a
        if ib != 0:
            res_b = res_b << ib
        final_res = adder(np.uint32(final_res), np.uint32(res_b))
        ib += 1
        b = b >> 1    
    return np.uint32(final_res)

def main():
    a = np.uint32(21)
    b = np.uint32(2)
    print(multiplier(a ,b))


if __name__ == "__main__":
    main()