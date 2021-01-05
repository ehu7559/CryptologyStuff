#Pollard P-1 RSA cracker

#Import Math
import math
#Helper Functions: Extended Euclidian Algorithm
def gcd(a,b):
    ''' (int a, int b)
        where a>b>0
        Recursively finds the greatest common factor of integers a and b'''
    bfactor = a//b
    remainder = a%b
    if remainder == 1:
        return 1
    elif remainder == 0:
        return b
    else:
        return gcd(int(b),int(remainder))

#Helper Functions: Modular Exponentiation (and auxiliary functions)
def powerRemainder(x,power,modulus):
    squarecount = int(math.log(power,2))
    val = x%modulus
    for i in range(1,squarecount+1):
        val = (val**2)%modulus
    multcount = power-(2**squarecount)
    initial = 2**squarecount

    #Calculate binsum and print
    pows = makebinsum(power)
    
    #Calculate output
    output = 1
    for i in pows:
        output = (output * squarepowremaux(x,i,modulus))%modulus
    return output

#Repeated Squaring function
def squarepowremaux(x,timessquared,modulus):
    val = x%modulus
    for i in range(timessquared):
        val = (val**2)%modulus
    return val

#Find the most efficient way to calculate a modular exponentiation result
def makebinsum(num):
    n = num
    output = []
    while n>0:
        newpow = int(math.log(n,2))
        if 2**newpow>n:
            newpow-=1
        n -= (2**newpow)
        output.insert(0,newpow)
    return output

#Given numbers (These specific integers were selected by a professor of mine)
nInput = int(input("Enter hex-string of key: "),16)          #Public key
cInput = int(input("Enter hex-string of ciphertext: "),16)   #ciphertext
eInput = int(input("Enter hex-string of exponent: "),16)   #Encryption exponent

def factorn(n):
    #Used Pollard p-1 method
    #Assume p-1 has only small prime factors (I'll check for 10000 factors)
    a = 2
    i = 0
    b = a
    d = 0 #just need d to exist for later
    smoothness = 10000
    while i < smoothness:
        i+=1
        b = powerRemainder(b, i, n) #b^i mod n
        d = gcd(b-1,n)
        if d>1:
            print("Found factor: "+str(d))
            break
    #List primes
    p = d
    q = n//d
    print("Factorization of n = "+str(p)+" * "+str(q))
    return [p,q]

def getDecryptionExponent(e,p,q):
    phi_n = (p-1)*(q-1)
    d = pow(e,-1,phi_n)
    print("Found Decryption Exponent: " + str(d))
    return d

def decryptMessage(c,d,n):
    '''(ciphertext, decryption_exponent, modulus) -> plaintext'''
    return powerRemainder(c,d,n)

def readCharacters(message):
    message = str(message) # Typecast the message to ensure stringiness
    alphabet = ' abcdefghijklmnopqrstuvwxyz'
    output = ''
    currchar = ''
    for digit in intstring:
        currchar += digit
        if len(currchar)==2:
            output+=alphabet[int(currchar)]
            currchar = ''
    return output

nfactors = factorn(nInput) #Factor the modulus
pIn = nfactors[0]
qIn = nfactors[1]
dIn = getDecryptionExponent(eInput,pIn,qIn)
mIn = decryptMessage(cInput, dIn, nInput)
pt = readCharacters(mIn)


print("Plaintext: " + pt)

