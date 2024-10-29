import string
import random
import itertools

key = ""
class DES:
    
    def permutate(text,key):
        charSplit = list(text)
        permutations = list(itertools.permutations(charSplit))
        permPos = random.randrange(0,len(permutations))
        key += str(permPos)
        perm = permutations[permPos]
        return perm
        
if __name__ == "__main__":
    encryption = DES.permutate("Hello", key)
    print(encryption)