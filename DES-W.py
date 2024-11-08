from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def des_encrypt(plaintext, key=None, iv=None):
    if key is None:
        key = get_random_bytes(8)  # Generate random 8-byte key if not provided
    if iv is None:
        iv = get_random_bytes(8)  # Generate random 8-byte IV if not provided

    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
    ciphertext = cipher.encrypt(padded_text)

    return ciphertext, key, iv


def des_decrypt(ciphertext, key, iv):
    decipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_padded_text = decipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, DES.block_size)
    return decrypted_text.decode('utf-8')


# Example usage
plaintext = "Hello, World!"

# Encrypt
ciphertext, key, iv = des_encrypt(plaintext)
print(f"Encrypted message: {ciphertext.hex()}")

# Decrypt
decrypted_message = des_decrypt(ciphertext, key, iv)
print(f"Decrypted message: {decrypted_message}")
