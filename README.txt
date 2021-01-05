Welcome to my Cryptology Folder!
CONTENTS:
1. Introduction
2. Password Mutation Generator (mutator.py)
3. Modular Arithmetic Helpers (modmath.py)
4. Affine/Caesar Cipher Helpers (affinecipher.py)
5. Vigenere Cipher Breaker (vigenerebreaker.py)
6. Pollard P-1 factoring RSA attacker (PollardAttack.py)
--------------------------------------------------------------------------------
INTRODUCTION:
This folder contains a small collection of Python programs I wrote to facilitate
my studies in cryptology.

While some of these programs originate from class projects, they are by no means
ground-breaking or unique to the course material. Releasing these projects does
not provide a solution to problems that do not have a variety of extant programs
that can do what my code does better. I've removed most of the dead code, but I
may have missed some. These programs are not mutually dependent. 

DISCLAIMER:
I take no responsibility for people who reuse my code to their own detriment. If
this code is found in someone's school project, they should reconsider their
academic integrity rather than blaming me for somehow enabling it as though this
made any difference when there were many programs already available. If anyone
is to blame, it is the student that decided MY code was somehow the best choice.
--------------------------------------------------------------------------------
PASSWORD MUTATION GENERATOR:
File: mutator.py
Suggested Usage: echo <base password> | python3 mutator.py > output.txt

The program takes in a single string and generates a list of reaonable mutations
of the password, with the mutations being either capitalization or replacement
with a similar-looking character. The mutation dictionary can be customized by
editing the mappings in the program. This is useful for brute-forcing over a 
small number of passwords, especially in the case of someone who is prone to
reuse variations of a password.
--------------------------------------------------------------------------------
MODULAR ARITHMETIC HELPERS:
File: modmath.py

This program contains a small number of useful modular arithmetic functions that
were written as a personal exercise when studying cryptology.
--------------------------------------------------------------------------------
AFFINE/CAESAR CIPHER HELPERS
File: affinecipher.py

This was written during my review of introductory cryptology material before the
semester began. It implements affine and caesar ciphers, as the name suggests.
--------------------------------------------------------------------------------
VIGENERE CIPHER BREAKER
File: vigenerebreaker.py
Suggested Usage: cat ciphertext.txt | python3 vigenerebreaker.py

This was written as a personal challenge to myself. Solutions already exist, but
this solution is my implementation
(This is my solution! There are many like it, but this one is MINE!)
--------------------------------------------------------------------------------
POLLARD P-1 FACTORING RSA ATTACKER
File: PollardAttack.py

This is code salvaged from my solution to a cryptology problem. I have upgraded
it to work with hexadecimal instead of decimal numbers. It assumes an a1z26
alphabet, but that can be remedied. As the name suggests, this implementation
uses the Pollard P-1 method.

