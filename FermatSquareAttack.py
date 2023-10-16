#FERMAT TRIANGULATION FACTORIZATION ATTACK

#Import Math
from sys import argv
from math import sqrt

#Helper Functions: Extended Euclidian Algorithm
def gcd(a: int, b : int):
    '''Memory-compact, iterative version of GCD using Extended Euclidian Algorithm'''
    if a == 0 or b == 0:
        raise Exception("Cannot find GCD with 0")
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a #Flip if they end up not matching.
    while a % b != 0:
        a, b = b, a % b
    return b

#Helper Functions: Modular Exponentiation (and auxiliary functions)
def mod_exp(b: int, x: int, n: int) -> int:
    if x < 0:
        b, x = mod_inv(b, n), -x
    acc = 1 #accumulator
    curr_pow = b
    while x > 0:
        acc *= 1 if (x % 2 == 0) else curr_pow
        acc = acc % n
        curr_pow = (curr_pow ** 2) % n
        x = x >> 2
    return acc

#MODULAR INVERSE:
def mod_inv(x, n):
    '''Computes x^-1 mod n'''
    #Compute GCD using EEA, saving values along the way.
    a, b = n, x
    eea_stack = [a, b]
    
    #Generate the stack.
    while a % b != 0:
        a, b = b, a % b
        eea_stack.append(b)

    #Raise an exception.
    if b != 1:
        raise Exception("Modular Inverse of " + str(x) + " does not exist mod " + str(n))

    eea_stack.pop() #Remove the last number (assumed to be a 1)

    high = 1
    low = -1 * (eea_stack[-2] // eea_stack[-1])
    while len(eea_stack) > 2:
        eea_stack.pop() #Remove an element
        ratio = eea_stack[-2] // eea_stack[-1]
        high, low = low, (high - (ratio * low))

    return low % n

def int_sqrt(n : int) -> int:
    '''A precise integer-based square root.\nWill effectively round down if n is not a perfect square'''
    curr = 1
    acc = 0
    while curr * curr < n:
        curr = curr << 1
    while curr:
        acc += curr
        if acc * acc > n:
            acc -= curr
        curr = curr >> 1
    return acc

#haha 1-liner
is_square = lambda x : (int_sqrt(x))**2 == x

def factorn(n : int, limit = None) -> int:
    a = int(sqrt(n))
    if limit is None:
        limit = a #Gets b^2 in the Fermat attack to just over n.
    for i in range(limit):
        rhs = (a + i)**2 - n
        if rhs < 0:
            continue
        b = int(sqrt(rhs)//1)
        #Adjustment for rounding errors Just in case, for large numbers.
        while b**2 < rhs: 
            b += 1
        print(f"i = {i}, b = {b} ",end = "\r")
        if b**2 == rhs:
            return ((a + i - b),(a + i + b))        
    raise Exception("Could not find factor!")

def getDecryptionExponent(e : int, p : int, q : int) -> int:
    '''COmputes the decryption exponent'''
    return mod_inv(e, (p-1)*(q-1))

if __name__ == "__main__":
    #USAGE: pollard_attack [encryption modulus] [encryption exponent] [limit (optional)]
    main_n = int(argv[1])
    main_e = int(argv[2])
    main_limit = None
    if len(argv) == 4:
        main_limit = int(argv[3])
    print("ATTEMPTING TO FACTOR MODULUS")
    main_p, main_q = factorn(main_n, limit=main_limit)
    print("\nCOMPUTING DECRYPTION EXPONENT")
    main_d = getDecryptionExponent(main_e, main_p, main_q)
    print("--- RESULTS ---")
    print(f"FACTORIZATION: {main_p} * {main_q} = {main_q * main_p}")
    print(f"DECRYPTION EXPONENT: {main_d}")
#EXAMPLE: fermatsquareattack 14590430507 65537 
