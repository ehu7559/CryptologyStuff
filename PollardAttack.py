#Pollard P-1 RSA cracker
'''
Originally written in Spring 2020 at UMD, CMSC456.

Modified heavily to make a general application rather than a test answer.
'''

#Import Math
from sys import argv
from time import sleep

#Helper Functions: Extended Euclidian Algorithm
def gcd(a: int, b : int):
    '''Fixed-space, iterative version of GCD using Extended Euclidian Algorithm'''
    a, b = abs(a), abs(b)
    a, b = max(a, b), min(a, b)
    assert (b > 0)
    while a % b:
        a, b = b, a % b
    return b

#Helper Functions: Modular Exponentiation (and auxiliary functions)
def mod_exp(b: int, x: int, n: int) -> int:
    '''Fixed-space O(lg(x))-time modular exponentiator.'''
    if x < 0:
        b, x = mod_inv(b, n), -x #Invert and negate for negative powers.
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

def factorn(n : int, smoothness = None) -> int:
    assert(n>0)
    #Uses Pollard p-1 method
    a = 2
    i = 0
    b = a
    d = 0 #just need d to exist for later
    solved = False
    while smoothness is None or i < smoothness:
        i+=1
        if i%1000==0: print(f"Smoothness Level: {i}", end="\r")
        b = pow(a, i, n)#mod_exp(a, i, n) #b^i mod n
        assert(b > 1)
        d = gcd(b-1,n)
        if d>1:
            print("Found factor: "+str(d)+ "\t\t\t\t")
            solved = True
            break
    if not solved:
        raise Exception("Could not factor modulus. Increase smoothness limit!")
    
    #List primes
    p = d
    q = n//d
    print(f"Factorization of n = {p} * {q}")
    return (p, q)

def getDecryptionExponent(e : int, p : int, q : int) -> int:
    return mod_inv(e, (p-1)*(q-1))

if __name__ == "__main__":
    #USAGE: pollard_attack [encryption modulus] [encryption exponent] [smoothness (optional)]
    main_n = int(argv[1])
    main_e = int(argv[2])
    main_smoothness = None
    if len(argv) == 4:
        main_smoothness = int(argv[3])
    print("ATTEMPTING TO FACTOR MODULUS")
    main_p, main_q = factorn(main_n, smoothness=main_smoothness)
    print("COMPUTING DECRYPTION EXPONENT")
    main_d = getDecryptionExponent(main_e, main_p, main_q)
    print("--- RESULTS ---")
    print(f"FACTORIZATION: {main_p} * {main_q}")
    print(f"DECRYPTION EXPONENT: {main_d}")
