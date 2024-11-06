import string
import random
import itertools

subkeys = [
    '01111111','10111111','11011111','11101111',
    '11110111','11111011','11111101','11111110',
    '10101010','01010101','10100101','01011010',
    '00001111','00110011','11001100','11110000'
]
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
            permList = permutations[permPos]
            for char in permList:
                perm.append(char)
        return perm
    
    # ***
    # converts the permuted text to a byte array
    # ***
    def convertToBytes(permText):
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
    key = DES.makeOneString(subkeys)
    encryption = DES.convertToBytes(DES.FirstPermutate("Hello World", key))
    result = DES.makeOneString(encryption)
    print(encryption)
    print(result)