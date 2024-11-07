from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

key = get_random_bytes(8)
iv = get_random_bytes(8)  # IV must be 8 bytes for DES

cipher = DES.new(key, DES.MODE_CBC, iv)

plaintext = "Hello, World!"
plaintext_bytes = plaintext.encode('utf-8')
padded_text = pad(plaintext_bytes, DES.block_size)

ciphertext = cipher.encrypt(padded_text)

print(f"Encrypted message: {ciphertext.hex()}")

# Decryption
decipher = DES.new(key, DES.MODE_CBC, iv)
decrypted_padded_text = decipher.decrypt(ciphertext)
decrypted_text = unpad(decrypted_padded_text, DES.block_size)
decrypted_message = decrypted_text.decode('utf-8')

print(f"Decrypted message: {decrypted_message}")
