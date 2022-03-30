import sys

mutdict = {
    'a':["A","4"],
    'b':["B","6"],
    'c':["C"],
    'd':["D"],
    'e':["E","3"],
    'f':["F"],
    'g':["G","9"],
    'h':["H"],
    'i':["I","1"],
    'j':["J"],
    'k':["K"],
    'l':["L","1"],
    'm':["M"],
    'n':["N"],
    'o':["O","0"],
    'p':["P"],
    'q':["Q"],
    'r':["R"],
    's':["S","5"],
    't':["T",'+'],
    'u':["U"],
    'v':["V"],
    'w':["W"],
    'x':["X"],
    'y':["Y"],
    'z':["Z"],
    '1':["!"],
    '2':["@"],
    '3':["#"],
    '4':["$"],
    '5':["%"],
    '6':["^"],
    '7':["&"],
    '8':["*"],
    '9':["("],
    '0':["O","o",")"]
    }
def mutset(character):
    if character in mutdict.keys():
        return mutdict[character]
    return []

pqueue = []

class Passo:

    def __init__(self, string, mutsleft,lastMut):
        self.string = string
        self.mutsLeft = mutsleft
        self.lastMut = lastMut
        
    def fractalize(self):
        if self.mutsLeft==0:
            return
        if self.lastMut == len(self.string)-1:
            return
        for i in range(self.lastMut+1, len(self.string)):
            replaceset = mutset(self.string[i])#Get mutation set
            for replacement in replaceset: #for each potential mutation
                new_str = self.string[:i] + replacement + self.string[i+1:]
                pqueue.append(Passo(new_str, self.mutsLeft-1, i))
def complexityOf(string):
    permutations = 1
    for character in string:
        if character in mutdict.keys():
            permutations *= (1 + len(mutset(character)))
        else:
            #Attempt to reverse mutation mappings
            possiblemuts = 0 
            for i in mutdict.keys():
                if character in mutdict[i]:
                    possiblemuts += len(mutdict[i])
            permutations *= (1 + possiblemuts)
    return permutations

def tryPass(prefix, password, suffix):
    print(prefix+password+suffix)

def attack(prefix, basepass, suffix):
    pqueue.append(Passo(basepass,len(basepass),-1))
    count = 0
    while len(pqueue)>0:
        x = pqueue.pop(0)
        tryPass(prefix,x.string,suffix)
        x.fractalize()
        count += 1
    return count

#Main function
if __name__ == "__main__":
    if len(sys.argv) == 4:
        attack(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: "+sys.argv[0]+" <prefix> <base password> <suffix>")
