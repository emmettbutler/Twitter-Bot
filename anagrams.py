#anagram.py: commandline tool for generating solvable and unsolvable anagrams of arbitrary length
#Emmett Butler 2011
import random

DICT_FILE = "/usr/share/dict/words"
words = [word.strip() for word in open(DICT_FILE, "r").readlines()]
vowels = ["a", "e", "i", "o", "u"]

#get_solvable: returns an anagram of length (length) made by scrambling a dictionary word
def get_solvable(length):
    word = list(random.choice(words)) #pick a random word
    while len(word) != length: #try again until the word matches the desired length
        word = list(random.choice(words))
    if (ord(word[0]) >= ord('A')) and (ord(word[0]) <= ord('Z')): #if the word starts with a capital letter
        word[0] = chr(ord(word[0]) + ord(' ')) #change the letter to lower case
    random.shuffle(word) #shuffle characters
    word = "".join(word)
    return word

#get_unsolvable: returns an anagram of length (length) proven to be unsolvable
def get_unsolvable(length):
    word = build_unsolvable(length) #attempt to generate unsolvable anagram
    while not is_unsolvable(word): #if the generated puzzle is solvable
        word = build_unsolvable(length) #try again
    return word

#build_unsolvable: returns a string of randomly selected characters of length (length)
def build_unsolvable(length):
    word = list()
    while len(word) < length:
        if random.choice(range(1, length)) == 1: #artificially increase the probability of a vowel as a function of length
            word.append(random.choice(vowels))
        else:
            word.append(chr(random.choice(range(ord('a'), ord('z')))))
    return "".join(word)

#is_unsolvable: returns false if (word) is an anagram of any dictionary word, true otherwise
def is_unsolvable(word):
    for x in words:
        if is_anagram(word, x):
            return False
    return True

#signature: returns an integer that is dependent on the occurrences of each letter in (word)
def signature(word):
    prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    signature = 1
    for i in list(word): #for each character
        if ord(i) - ord('a') >= 0:
            signature *= prime[ord(i) - ord('a')] #multiply the total by the corresponding prime number
    return signature

#is_anagram: returns true if (str1) and (str2) are anagrams of each other, false otherwise
def is_anagram(str1, str2):
    return signature(str1) == signature(str2)

