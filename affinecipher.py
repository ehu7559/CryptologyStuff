ALPHABET = "abcdefghijklmnopqrstuvwxyz" #Feel free to chance your character set as needed.

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

valid_affine_factors = filter(lambda x : (gcd(x, len(ALPHABET)) == 1), range(1, len(ALPHABET)))

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

#Generate alphabet->index lookup tables
ALPHANUM = {y : x for (x, y) in enumerate(list(ALPHABET), start=1)}
NUMALPHA = {x : y for (x, y) in enumerate(list(ALPHABET), start=1)}

#Single-character encryption function
def apply_affine(char, key):
    a, b = key
    if char not in ALPHABET:
        return char
    return NUMALPHA[(((a * ALPHANUM[char]) + b) % len(ALPHABET))]

def apply_deaffine(char, key):
    a, b = key
    if gcd(a, len(ALPHABET)) != 1:
        raise Exception("Destructive Affine key used. Cannot decrypt.")
    a = mod_inv(a, len(ALPHABET))
    if char not in ALPHABET:
        return char
    return NUMALPHA[((a * ((ALPHANUM[char] - b ) % len(ALPHABET))) % len(ALPHABET))]

#Encipher/decipher functions
def affine(text : str, key):
    return "".join([apply_affine(c, key) for c in list(text)])

def deaffine(text : str, key):
    return "".join([apply_deaffine(c, key) for c in list(text)])
