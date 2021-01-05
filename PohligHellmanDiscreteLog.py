#Exam 2 Question 2
import math

#Helper Functions: Extended Euclidian Algorithm
def gcd(a,b,showWork = False):
    ''' (int a, int b)
        where a>b>0
        Recursively finds the greatest common factor of integers a and b'''
    bfactor = a//b
    remainder = a%b
    if showWork:
        print(str(a) + " = " + str(bfactor) + " * " + str(b) + " + " + str(remainder))
    if remainder == 1:
        return 1
    elif remainder == 0:
        return b
    else:
        return gcd(int(b),int(remainder),showWork)
p = int(input("Enter Modulus ('p') in decimal form: "))
a = int(input("Enter Log Base ('a') in decimal form: "))
b = int(input("Enter Log Argument ('b') in decimal form: "))

# --- Pohlig-Hellman Attack ---
factordict = {}
num = p-1
currfac = 0
smoothness = 1000
for i in range(2,smoothness):
    if num == 1 or num < i:
        break
    if (num%i == 0):
        factordict[i] = 0
        while(num%i == 0):
            num = num//i
            factordict[i] += 1

xmoddict = {}
for q in factordict.keys():
    qxset = []
    r = factordict[q]
    exp = (p-1)//q
    Beta = b
    Betaraised = pow(Beta,exp,p)
    Alphabase = pow(a, exp, p)
    alphas = []
    for i in range(q):
        alphanew = pow(Alphabase, i, p)
        alphas.append(alphanew)
    for k in range(q):
        if alphas[k] == Betaraised:
            qxset.append(k)
            break
    for anr in range(1,r):
        alphapow = -1 * qxset[anr-1] * (pow(q,anr-1))
        alphamult = pow(a, alphapow,p)
        Beta *= alphamult
        betapow = exp//(pow(q,anr))
        Betaraised = pow(Beta,betapow,p)
        for k in range(q):
            if alphas[k] == Betaraised:
                qxset.append(k)
                break
    xhere = 0
    for j in range(len(qxset)):
        newterm = qxset[j] * (q**j)
        xhere = (xhere + newterm)%(q**r)
    xmoddict[xhere] = q**r

N = p-1
x = 0
for c in xmoddict.keys():
    y = N//xmoddict[c]
    z = pow(y,-1,xmoddict[c])
    x = (x + (c * y * z)) % N
    
print("L_a(b) = "+str(x))
