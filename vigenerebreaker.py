from sys import argv
alphabet = "abcdefghijklmnopqrstuvwxyz"

#Allow constant time character lookup (Minor speed increase for minimal overhead at start)
charnumlookup = {}
for i in range(len(alphabet)):
    charnumlookup[alphabet[i]] = i

#Scoring frequency based on frequency analysis
scores = {'e': 120, 't': 90, 'a': 80, 'i': 80, 'n': 80, 'o': 80, 's': 80, 'h': 64, 'r': 62, 'd': 44, 'l': 40, 'u': 34, 'c': 30, 'm': 30, 'f': 25, 'w': 20, 'y': 20, 'g': 17, 'p': 17, 'b': 16, 'v': 12, 'k': 8, 'q': 5, 'j': 4, 'x': 4, 'z': 2}

def score_text(txt: str) -> int:
    return sum([scores[x] for x in sanitize(txt)])

#Helper Methods for normal vigenere operations
def sanitize(txt : str) -> str:
    '''Removes all offending characters to avoid processing them'''
    output = ""
    for achar in txt:
        if achar in alphabet:
            output+=achar
    return output

def tonum(char : str) -> int :
    '''converts character to corresponding integer value'''
    return charnumlookup[char]

def tochar(num : int) -> str:
    '''converts integer to corresponding character value
    has an added safeguard to prevent overflow'''
    return alphabet[num%(len(alphabet))]

def encrypt(text: str, key : str):
    output = ""
    key_ptr = 0
    for i in range(len(text)):
        if text[i] in alphabet:
            output += tochar(tonum(text[i].lower()) + tonum(key[key_ptr].lower()))
            key_ptr = (key_ptr + 1) % len(key)
            continue
        output += text[i]
    return output

def decrypt(text: str, key : str):
    output = ""
    key_ptr = 0
    for i in range(len(text)):
        if text[i] in alphabet:
            output += tochar(tonum(text[i].lower()) - tonum(key[key_ptr].lower()))
            key_ptr = (key_ptr + 1) % len(key)
            continue
        output += text[i]
    return output

def kasiski_analysis(text: str) -> int:
    text = sanitize(text)
    best_score = 0
    best_shift = 0
    wrap_text = str(text)
    for i in range(len(text)):
        wrap_text = wrap_text[-1] + wrap_text[:-1]
        i_score = 0
        for j in range(len(text)):
            i_score += 1 if text[j] == wrap_text[j] else 0
        if i_score > best_score and i % best_score != 0:
            best_score = i_score
            best_shift = i
        
    #Catch
    if best_shift == 0:
        raise Exception("Text is resistant to Kasiski Analysis")
    return best_shift

def guess_key_char(text: str) -> str:
    best_char = None
    best_score = 0
    for a in alphabet:
        a_score = score_text(encrypt(text, a))
        if a_score > best_score:
            best_score = a_score
            best_char = a
    return a

def guess_key(text: str) -> str:
    key_str = ""
    key_length = kasiski_analysis(sanitize(text))
    
    sub_sections = ["" for i in range(key_length)]
    for i in range(len(text)):
        sub_sections[i % key_length] += text[i]

    for i in range(key_length):
        key_str += guess_key_char(sub_sections[i])
    
    return key_str

def crack_text(text: str) -> str:
    return decrypt(text, guess_key(text))

if __name__ == "__main__":
    if len(argv) == 1:
        raise Exception("Usage: vigenerbreaker [text to break]")
    text_to_break = None
    if len(argv) == 2:
        text_to_break = argv[1]
    else:
        text_to_break = " ".join([str(a) for a in argv[1:]])
    print(crack_text(text_to_break))
