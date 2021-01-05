import math

alphabet = "abcdefghijklmnopqrstuvwxyz"
#Allow constant time character lookup (Minor speed increase for minimal overhead at start)
charnumlookup = {}
for i in range(len(alphabet)):
    charnumlookup[alphabet[i]] = i
#Helper Methods for normal vigenere operations
def sanitize(txt):
    '''Removes all offending characters to avoid processing them'''
    output = ""
    for achar in txt:
        if achar in alphabet:
            output+=achar
    return output

def tonum(char):
    '''converts character to corresponding integer value'''
    return charnumlookup[char]

def tochar(num):
    '''converts integer to corresponding character value
    has an added safeguard to prevent overflow'''
    return alphabet[num%(len(alphabet))]

def encryptchar(chara,charb):
    return tochar((tonum(chara)+tonum(charb))%(len(alphabet)))

def decryptchar(chara, charb):
    difference = tonum(chara)-tonum(charb)
    if difference<0:
        difference += len(alphabet)
    return tochar(difference)

#Vigenere Encrypt and Decrypt Functions
def encrypt(plaintext,key):
    text = sanitize(plaintext)
    keyindex = 0
    output = ''
    keysize = len(key)
    if keysize==0:
        return text
    #Encrypt character by character
    for achar in text:
        output+= encryptchar(achar,key[keyindex])
        keyindex = (keyindex+1)%keysize
    return output

def decrypt(plaintext,key):
    text = sanitize(plaintext)
    keyindex = 0
    output = ''
    keysize = len(key)
    if keysize==0:
        return text
    #Encrypt character by character
    for achar in text:
        output+= decryptchar(achar,key[keyindex])
        keyindex = (keyindex+1)%keysize
    return output
#Helper functions for Kasiski Examination
def cycle(text,index):
    '''cycles a text, helper function for Kasiski Examination'''
    if len(text)<2:
        return text
    n = index%len(text)
    if n==0:
        return text
    return text[n:len(text)-1]+text[0:n-1]

def countaligned(stra,strb):
    '''counts the number of aligned characters in two strings'''
    minlength = min(len(stra),len(strb))
    output = 0
    for i in range(minlength):
        if stra[i]==strb[i]:
            output+=1
    return output

def kasiskiShift(text,num):
    '''returns the number of alignments between text and a num-cycled text'''
    return countaligned(text,cycle(text,num))

def factors(n):
    '''Factor listing valid for reasonable-length keys'''
    output = []
    for i in range(1,n//2 + 1):
        if n%i == 0:
            output.append(i)
    return output

def kasiskiExamination(text):
    '''Returns probable key sizes with reliability dependent on text'''
    #Alignment mapping of the whole text
    kasiskiFrequencies = [0] #To pad for no-shift, but not count ti.
    for i in range(1,len(text)-1):
        kasiskiFrequencies.append(kasiskiShift(text,i))
    
    #Look for maximum and return it
    maxvalue = max(kasiskiFrequencies)
    maxindex = kasiskiFrequencies.index(maxvalue)

    return maxindex

#Actual Key Guessing
englishFrequencies = "etaoinsrhldcumfpgwybvkxjqz"

def breaksets(string,keysize):
    index = 0
    output = []
    for i in range(keysize):
        output.append("")
    for j in string:
        output[index]+=j
        index = (index+1)%keysize
    return output

def countchars(text):
    '''frequency analysis'''
    output = {}
    for i in alphabet:
        output[i] = 0
    for achar in text:
        if achar in alphabet:
            output[achar] += 1
    return output
    
def guessKeyChar(charset):
    '''assume most common is e. A pretty reliable guess as to the character used to encrypt this set'''
    frequencies = countchars(charset)
    
    #Find most frequent character
    maxcount = 0
    maxletter = ""
    for letter in alphabet:
        if frequencies[letter]>maxcount:
            maxletter = letter
            maxcount = frequencies[letter]

    #Decrypt the maxletter. change the e to the next most common if wrong.
    return decryptchar(maxletter,"e")

def guessKey(text,size):
    output = ""
    charsets = breaksets(text,size)
    for aset in charsets:
        output+=guessKeyChar(aset)
    return output
#Run it on the given ciphertext
def main():
    ciphertext = input("Enter Ciphertext: ")
    print("--- INITIALIZING VIGENERE BREAKER ---")
    print("TEXT: "+ciphertext)
    print("--- BEGINNING KASISKI ANALYSIS OF TEXT ---")
    probablekeysize = kasiskiExamination(ciphertext)
    print("KEY SIZE GUESS: "+ str(probablekeysize))
    keysizefactors = factors(probablekeysize)
    print("FACTOR LIST: "+str(keysizefactors))
    print("--- BEGINNING KEY GUESSING BASED ON SIZES ---")
    for i in keysizefactors:
        print("PROCESSING GUESS FOR KEY SIZE: "+str(i))
        keyguessforsize = guessKey(ciphertext,i)
        print("GUESS: " + keyguessforsize)
        print("GUESSED DECRYPTION: "+ decrypt(ciphertext,keyguessforsize))
    print("--- FINISHED ---")
main()
