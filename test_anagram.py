import sys
import anagrams

if len(sys.argv) == 3:
    if sys.argv[1] == "t":
        print anagrams.get_solvable(int(sys.argv[2]))
    elif sys.argv[1] == "f":
        print anagrams.get_unsolvable(int(sys.argv[2]))
else:
    print "Usage: anagram.py <solvable [t|f]> <length>"
