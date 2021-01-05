ALPHANUM = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,
            'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
NUMALPHA = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
affinefactors = [1,3,5,7,9,11,15,17,19,21,23,25]

def setalphabet(string):
    '''overwrites the alphabet'''
    global ALPHABET,NUMALPHA,ALPHANUM
    ALPHABET = string
    NUMALPHA = " "+string
    index = 0
    for character in alphabet:
        index +=1
        ALPHANUM[character] = index
    return None


def chartonum(character):
    '''string -> int\n enumerates A1Z26 a character in constant time.'''
    if character in ALPHABET:
        return ALPHANUM[character]
    return 0

def chardistance(a,b):
    return (chartonum(a)-chartonum(b))

def caesarshift(text,shift):
    '''string, int -> string\n Caesar-shifts text with shift shift.'''
    output = ""
    for achar in text:
        if not(achar in ALPHABET):
            output+=achar
        else:
            shiftindex = (chartonum(achar)+shift-1)%26
            output+= ALPHABET[shiftindex]

    return output

def allshifts(text):
    '''string -> string.'''
    output = ""
    for i in range(len(ALPHABET)):
        output+= caesarshift(text,i)+'\n'
    return output

def a1z26(string):
    '''string -> int[]\n a1-z26 encodes all alphanumeric characters.\nAll others are replaced with 0'''
    output = []
    for char in string:
        output.append(chartonum(char))
    return output

def a0z25(string):
    output = []
    for char in string:
        output.append(chartonum(char)-1)
    return output

def affine(string,a,b):
    '''string,int,int -> string\n Affine cipher with a0z25 mod 26'''
    output = ""
    toks = a0z25(string)
    for token in toks:
        output+=ALPHABET[((token)*a+b)%26]
    return output

def deaffine(string,a,b):
    '''string, int, int -> string\n Decrypt affine cipher with a0z25 mod 26'''
    output = ""
    toks = a0z25(string)
    for token in toks:
        lettertoken = token-b
        addcounter = 0
        fintoken = 0
        if a==0:
            fintoken = 0
        else:
            while lettertoken%a > 0 and addcounter<26:
                lettertoken+=26
                addcounter+=1
            fintoken = lettertoken//a
        output+=ALPHABET[fintoken]
    return output

def sanitize(string):
    output = ""
    for c in string:
        if c in ALPHABET:
            output += c
    return output 
