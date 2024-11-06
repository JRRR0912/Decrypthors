import string
import random
import itertools

key = ""
class DES:
    
    # ***
    # with this method, the input plaintext 
    # goes through the initial permutation
    # ***
    def FirstPermutate(text,key):
        perm = list()
        wordSplit = text.split()
        for word in wordSplit:
            charSplit = list(word)
            permutations = list(itertools.permutations(charSplit))
            permPos = random.randrange(0,len(permutations))
            key += str(permPos)
            permList = permutations[permPos]
            for char in permList:
                perm.append(char)
        return perm
    
    # ***
    # converts the permuted text to a byte array
    # ***
    def convertToBytes(permText, key):
        byteList = list()
        for byte in permText:
            byteList.append(format(ord(byte), '08b'))
        return byteList
        
    def makeOneString(byteList):
        binaryString = ""
        for byte in byteList:
            binaryString += byte
        return binaryString
    
if __name__ == "__main__":
    encryption = DES.convertToBytes(DES.FirstPermutate("Hello World", key), key)
    result = DES.makeOneString(encryption)
    print(encryption)
    print(result)