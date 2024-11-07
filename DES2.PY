import string
import random
import itertools
import secrets

key = secrets.token_bytes(8)


S_Boxes = [
    [
        [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0],
        [14,12,10,8,6,4,2,0,1,3,5,7,9,11,13,15],
        [15,0,14,1,13,2,12,3,11,4,10,5,9,6,8,7],
        [7,15,6,14,5,13,4,12,3,11,2,10,1,9,0,8]
    ],
    [
        [7,15,6,14,5,13,4,12,3,11,2,10,1,9,0,8],
        [15,0,14,1,13,2,12,3,11,4,10,5,9,6,8,7],
        [14,12,10,8,6,4,2,0,1,3,5,7,9,11,13,15],
        [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0]
    ],
    [
        [15,0,14,1,13,2,12,3,11,4,10,5,9,6,8,7],
        [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0],
        [7,15,6,14,5,13,4,12,3,11,2,10,1,9,0,8],
        [14,12,10,8,6,4,2,0,1,3,5,7,9,11,13,15]
    ],
    [
        [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0],
        [15,0,14,1,13,2,12,3,11,4,10,5,9,6,8,7],
        [14,12,10,8,6,4,2,0,1,3,5,7,9,11,13,15],
        [7,15,6,14,5,13,4,12,3,11,2,10,1,9,0,8]   
    ],
    [
        [8,7,9,6,10,5,11,4,12,3,13,2,14,1,15,0],
        [15,0,14,1,13,2,12,3,11,4,10,5,9,6,8,7],
        [7,15,6,14,5,13,4,12,3,11,2,10,1,9,0,8],
        [14,12,10,8,6,4,2,0,1,3,5,7,9,11,13,15]
    ],
    [
        [5,2,15,10,4,8,13,0,7,11,3,14,9,12,1,6],
        [7,10,3,15,0,12,4,1,13,2,14,3,9,5,8,6,11],
        [11,7,0,15,10,2,8,1,14,3,12,4,11,5,9,6,13],
        [8,4,15,10,0,3,11,7,14,2,9,12,13,6,1,5]
    ],
    [
        [8,4,15,10,0,3,11,7,14,2,9,12,13,6,1,5],
        [11,7,0,15,10,2,8,1,14,3,12,4,11,5,9,6,13],
        [7,10,3,15,0,12,4,1,13,2,14,3,9,5,8,6,11],
        [5,2,15,10,4,8,13,0,7,11,3,14,9,12,1,6]
    ],
    [
        [7,10,3,15,0,12,4,1,13,2,14,3,9,5,8,6,11],
        [8,4,15,10,0,3,11,7,14,2,9,12,13,6,1,5],
        [5,2,15,10,4,8,13,0,7,11,3,14,9,12,1,6],
        [11,7,0,15,10,2,8,1,14,3,12,4,11,5,9,6,13]
    ]
]
class schedule:
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
        key = schedule.permute(initial_key, schedule.PC1)
        
        # Split the key into left and right halves
        left, right = key[:28], key[28:]
        round_keys = []

        for i in range(16):
            # Rotate left halves
            left = schedule.left_rotate(left, schedule.ROTATIONS[i])
            right = schedule.left_rotate(right, schedule.ROTATIONS[i])
            
            # Combine halves and permute with PC2 to get the round key
            combined_key = left + right
            round_key = schedule.permute(combined_key, schedule.PC2)
            round_keys.append(round_key)

        return round_keys
    
subKeys = schedule.generate_round_keys(key)

class DES:
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
    
    def split_into_blocks(text, block_size=8):
        """Split input text into blocks of a specified size, padding if necessary."""
        # Ensure input is bytes
        text = text.encode() if isinstance(text, str) else text

        # Apply padding to make text a multiple of the block size
        padded_text = DES.pad(text, block_size)
        
        # Split into blocks
        blocks = [padded_text[i:i + block_size] for i in range(0, len(padded_text), block_size)]
        return blocks
    
    def s_box_substitute(s_box, six_bits):
        """Apply an S-box to a 6-bit input."""
        # Extract row (first and last bits)
        row = (six_bits & 0b100000) >> 4 | (six_bits & 0b000001)
        # Extract column (middle 4 bits)
        col = (six_bits & 0b011110) >> 1
        # Perform substitution
        return s_box[row][col]
    
    def apply_s_boxes(s_boxes, input_48_bits):
        """Apply all 8 S-boxes to a 48-bit input, returning a 32-bit output."""
        output = 0
        # Divide the input into 8 blocks of 6 bits each
        for i in range(8):
            # Extract 6-bit block for the current S-box
            six_bits = (input_48_bits >> (42 - 6 * i)) & 0b111111
            # Substitute using the S-box and get the 4-bit result
            substituted_bits = DES.s_box_substitute(s_boxes[i], six_bits)
            # Shift and combine into the 32-bit output
            output = (output << 4) | substituted_bits
        return output
    
    def encryptBlocks(blockList):
        
        for block in blockList:
            DES.FirstPermutate(block)
            DES.apply_s_boxes(S_Boxes,block)
            

if __name__ == "__main__":
    input = "HELLO"
    blockList = DES.split_into_blocks(input,8)
    DES.encryptBlocks(blockList)
    