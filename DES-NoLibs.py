# DES Implementation in Pure Python

# Permutation tables and S-boxes
# ----------------------------------

# Initial Permutation (IP) table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation (FP) table (inverse of IP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9,  49, 17, 57, 25
]

# Permutation Choice 1 (PC-1) table
PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

# Permutation Choice 2 (PC-2) table
PC_2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of left shifts per round
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

# Expansion table
E = [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# S-boxes
S_BOX = [
    # S-box 1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    # S-box 2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    # S-box 3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    # S-box 4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    # S-box 5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    # S-box 6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    # S-box 7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    # S-box 8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

# P-box permutation table
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1,  15, 23, 26,
    5,  18, 31, 10,
    2,  8,  24, 14,
    32, 27, 3,  9,
    19, 13, 30, 6,
    22, 11, 4,  25
]

# DES Implementation in Pure Python

# [All the permutation tables, S-boxes, and helper functions remain unchanged]

# ... [Permutation tables and S-boxes as previously defined]

# Helper Functions
# ----------------------------------

def string_to_bit_array(text):
    """Converts a string into a list of bits."""
    bit_array = []
    for char in text:
        binval = bin(ord(char))[2:].rjust(8, '0')
        bit_array.extend([int(x) for x in binval])
    return bit_array

def bit_array_to_string(bit_array):
    """Converts a list of bits into a string."""
    res = ''
    for i in range(0, len(bit_array), 8):
        byte = bit_array[i:i+8]
        byte_str = ''.join([str(bit) for bit in byte])
        res += chr(int(byte_str, 2))
    return res

def permute(block, table):
    """Permutes a block of bits using a given table."""
    return [block[i - 1] for i in table]

def left_shift(bits, n):
    """Performs a circular left shift on a list of bits."""
    return bits[n:] + bits[:n]

def xor(t1, t2):
    """Performs a bitwise XOR on two lists of bits."""
    return [a ^ b for a, b in zip(t1, t2)]

def split_bits(bits, n):
    """Splits a list of bits into n-sized chunks."""
    return [bits[i:i + n] for i in range(0, len(bits), n)]

# Key Generation Functions
# ----------------------------------

def generate_keys(key_bits):
    """Generates 16 subkeys from the original key."""
    keys = []
    key = permute(key_bits, PC_1)
    left, right = key[:28], key[28:]
    for shift in SHIFT_SCHEDULE:
        left = left_shift(left, shift)
        right = left_shift(right, shift)
        combined = left + right
        round_key = permute(combined, PC_2)
        keys.append(round_key)
    return keys

# Feistel Function
# ----------------------------------

def substitute(sboxes, expanded_half_block):
    """Applies S-box substitution to the expanded half-block."""
    sub_blocks = split_bits(expanded_half_block, 6)
    result = []
    for i, block in enumerate(sub_blocks):
        row = int(f"{block[0]}{block[5]}", 2)
        column = int(''.join([str(x) for x in block[1:5]]), 2)
        val = sboxes[i][row][column]
        binval = bin(val)[2:].rjust(4, '0')
        result.extend([int(x) for x in binval])
    return result

def feistel(right, subkey):
    """The Feistel (F) function."""
    expanded_right = permute(right, E)
    temp = xor(expanded_right, subkey)
    sbox_substituted = substitute(S_BOX, temp)
    permuted = permute(sbox_substituted, P)
    return permuted

# Encryption and Decryption Functions
# ----------------------------------

def des_encrypt_block(block, keys):
    """Encrypts a single block of data."""
    block = permute(block, IP)
    left, right = block[:32], block[32:]
    for i in range(16):
        temp_right = right
        right = xor(left, feistel(right, keys[i]))
        left = temp_right
    combined = right + left  # Swap left and right
    encrypted_block = permute(combined, FP)
    return encrypted_block

def des_decrypt_block(block, keys):
    """Decrypts a single block of data."""
    block = permute(block, IP)
    left, right = block[:32], block[32:]
    for i in range(15, -1, -1):
        temp_right = right
        right = xor(left, feistel(right, keys[i]))
        left = temp_right
    combined = right + left  # Swap left and right, same as in encryption
    decrypted_block = permute(combined, FP)
    return decrypted_block

def des_encrypt(plaintext, key):
    """Encrypts plaintext using DES."""
    plaintext_bits = string_to_bit_array(plaintext)
    key_bits = string_to_bit_array(key)
    # Adjust key to 64 bits
    if len(key_bits) < 64:
        key_bits += [0] * (64 - len(key_bits))
    else:
        key_bits = key_bits[:64]
    # Generate subkeys
    keys = generate_keys(key_bits)
    # Pad plaintext to be multiple of 64 bits
    while len(plaintext_bits) % 64 != 0:
        plaintext_bits += [0]
    encrypted_bits = []
    for i in range(0, len(plaintext_bits), 64):
        block = plaintext_bits[i:i+64]
        encrypted_block = des_encrypt_block(block, keys)
        encrypted_bits.extend(encrypted_block)
    return encrypted_bits

def des_decrypt(ciphertext_bits, key):
    """Decrypts ciphertext using DES."""
    key_bits = string_to_bit_array(key)
    # Adjust key to 64 bits
    if len(key_bits) < 64:
        key_bits += [0] * (64 - len(key_bits))
    else:
        key_bits = key_bits[:64]
    # Generate subkeys
    keys = generate_keys(key_bits)
    decrypted_bits = []
    for i in range(0, len(ciphertext_bits), 64):
        block = ciphertext_bits[i:i+64]
        decrypted_block = des_decrypt_block(block, keys)
        decrypted_bits.extend(decrypted_block)
    return decrypted_bits

# Main Execution
# ----------------------------------

if __name__ == "__main__":
    plaintext = "Hello, World!"
    key = "secret_k"
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")

    # Encrypt
    encrypted_bits = des_encrypt(plaintext, key)
    # Convert encrypted bits to hexadecimal string
    encrypted_hex = ''.join('{:02x}'.format(int(''.join(map(str, encrypted_bits[i:i+8])), 2)) for i in range(0, len(encrypted_bits), 8))
    print(f"Encrypted (hex): {encrypted_hex}")

    # Decrypt
    decrypted_bits = des_decrypt(encrypted_bits, key)
    decrypted_text = bit_array_to_string(decrypted_bits).rstrip('\x00')  # Remove padding null bytes
    print(f"Decrypted text: {decrypted_text}")

