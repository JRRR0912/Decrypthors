import string
import random
import itertools
import secrets

subkeys = [
    '01111111','10111111','11011111','11101111',
    '11110111','11111011','11111101','11111110',
    '10101010','01010101','10100101','01011010',
    '00001111','00110011','11001100','11110000'
]
key = secrets.token_bytes(8)
class DES:
    
    # DES key schedule implementation
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27,
        19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29,
        21, 13, 5,  28, 20, 12, 4
    ]

    PC2 = [
        14, 17, 11, 24, 1,  5,
        3,  28, 15, 6,  21, 10,
        23, 19, 12, 4,  26, 8,
        16, 7,  27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    ROTATIONS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def permute(key, table):
        """Permute the key according to a table."""
        return [key[i - 1] for i in table]

    def left_rotate(bits, n):
        """Perform a circular left shift."""
        return bits[n:] + bits[:n]

    def generate_round_keys(initial_key):
        """Generate 16 round keys for DES encryption."""
        # Initial permutation of the key using PC1
        key = DES.permute(initial_key, DES.PC1)
        
        # Split the key into left and right halves
        left, right = key[:28], key[28:]
        round_keys = []

        for i in range(16):
            # Rotate left halves
            left = DES.left_rotate(left, DES.ROTATIONS[i])
            right = DES.left_rotate(right, DES.ROTATIONS[i])
            
            # Combine halves and permute with PC2 to get the round key
            combined_key = left + right
            round_key = DES.permute(combined_key, DES.PC2)
            round_keys.append(round_key)

        return round_keys

    # # Example usage with a sample 64-bit key (converted to a bit array)
    # initial_key = [int(b) for b in "{:064b}".format(0x133457799BBCDFF1)]
    # round_keys = generate_round_keys(initial_key)

    # # Print round keys in hexadecimal
    # for i, round_key in enumerate(round_keys, 1):
    #     print(f"Round {i} key:", ''.join(str(b) for b in round_key))

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
    
    def combineBytes(byteList):
        byteList = [b.encode() if isinstance(b, str) else b for b in byteList]
        return b''.join(byteList)
    
    def pad(data, block_size):
        """Pad data to a multiple of block_size using PKCS#7 padding."""
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def unpad(padded_data, block_size):
        """Remove PKCS#7 padding from data."""
        padding_length = padded_data[-1]
        if padding_length < 1 or padding_length > block_size:
            raise ValueError("Invalid padding.")
            # Check all padding bytes
        if padded_data[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Invalid padding.")
        return padded_data[:-padding_length]

if __name__ == "__main__":
    key = DES.makeOneString(subkeys)
    encryption = DES.convertToBytes(DES.FirstPermutate("Hello World", key))
    result = DES.makeOneString(encryption)
    
    print(encryption)
    print(result)
    print(DES.pad(DES.combineBytes(encryption),8))