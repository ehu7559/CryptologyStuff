'''
A lightweight simple modular arithmetic module for academic purposes.
Use math.pow() and other functions for serious things.
All quantities are assumed to be integers.
'''

import math

def gcd(a: int, b : int):
    ''' GCD using Extended Euclidian Algorithm'''
    if a == 0 or b == 0:
        raise Exception("Cannot find GCD with 0")
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    while a % b != 0:
        a, b = b, a % b
    return b

#Much faster, more compact, and very, very efficient.
def mod_exp(b: int, x: int, n: int) -> int:
    '''Computes residue class b ** x mod n, where all are non-negative integers'''
    if x == 0:
        return 1 #Simple catch case
    acc = 1 #accumulator
    curr_pow = b
    while x > 0:
        acc *= 1 if (x % 2 == 0) else curr_pow
        acc = acc % n
        curr_pow = (curr_pow ** 2) % n
        x = x // 2
    return acc

def factorsof(num):
    #Simple factorization
    output=[]
    for i in range(1,int(math.sqrt(num))+1):
        if num % i == 0:
            output.append(i)
            output.append(num//i)
    return output

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

def gcf(a,b):
    ''' Alias for Greatest Common Factor -> Greatest Common Denominator'''
    return gcd(a,b)

def lcm(a: int, b: int) -> int:
    '''Returns the least common multiple of two integers'''
    return (max(a,b) // gcd(a,b))*min(a,b)

def ascending_primes():
    yield 2
    yield 3
    prim_prod = 6
    pointer = 6
    while True:
        if gcd(pointer - 1, prim_prod) == 1:
            yield pointer - 1
            prim_prod *= pointer - 1
        if gcd(pointer + 1, prim_prod) == 1:
            yield pointer + 1
            prim_prod *= pointer + 1
        pointer += 6

def prime_factors(num):
    prime_stream = ascending_primes()
    p = next(prime_stream)
    factors = []
    while p < int(math.sqrt(num) + 1):
        if num % p == 0:
            factors.append(p)
            while num % p == 0:
                num = num // p

        p = next(prime_stream)

    #if the factor is still non-zero (means large prime factor)
    if num != 1:
        factors.append(num)
    
    return factors

def amoeba(num):
    prime_gen = ascending_primes()
    for i in range(num):
        print(next(prime_gen))
