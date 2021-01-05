import math

def extendedEuclidian(a,b):
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
        return extendedEuclidian(b,remainder)

def powerRemainder(x,power,modulus):
    ''' given int x, int power, int modulus --> x^p mod modulus'''
    squarecount = int(math.log(power,2)) # Gets the number of times you have to square the x.
    val = x%modulus #initialize x mod n
    for i in range(1,squarecount+1):
        val = (val**2)%modulus #calculates the repeated squares of x mod n (x^(2^i) mod n)
        print(str(x)+"^"+str(2**i)+" = "+str(val) + " mod " + str(modulus))

    #Calculate binsum and print
    pows = makebinsum(power) #break the power into a binary number so i can create it out of modular squares
    print("Following powers of two add to the specified power:\n" + str(pows))

    
    #Calculate output
    output = 1 #Initializes output
    for i in pows:
        output = (output * squarepowremaux(x,i,modulus))%modulus
    return output

def squarepowremaux(x,timessquared,modulus):
    val = x%modulus
    for i in range(timessquared):
        val = (val**2)%modulus
    print(str(x)+"^"+str(2**timessquared)+" = "+str(val) + " mod " + str(modulus))
    return val

def floorlog(num,base=2):
    output = int(math.log(num,2))
    if base**output > num:
        output-=1
    return output

def makebinsum(num):
    n = num
    output = []
    while n>0:
        newpow = floorlog(n,2)
        n -= (2**newpow)
        output.insert(0,newpow)
    return output

def factorsof(num):
    output=[]
    for i in range(1,int(math.sqrt(num))+1):
        if num%i == 0:
            output.append(i)
            output.append(num//i)
    return output

def gcf(a,b):
    return extendedEuclidian(a,b)

def lcm(a,b):
    return (a*b)/gcf(a,b)
