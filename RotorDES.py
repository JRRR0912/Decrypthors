import string
import random
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# Helper functions for DES
def pad_text(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def des_encrypt(plain_text, key):
    des = DES.new(key, DES.MODE_ECB)
    padded_text = pad_text(plain_text)
    encrypted_text = des.encrypt(padded_text.encode('utf-8'))
    return encrypted_text

def des_decrypt(encrypted_text, key):
    des = DES.new(key, DES.MODE_ECB)
    decrypted_text = des.decrypt(encrypted_text).strip()
    return decrypted_text.decode('utf-8')

# Helper function to create a randomized alphabet rotor
def create_rotor():
    alphabet = string.ascii_uppercase
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return ''.join(shuffled)

# Class for the Rotor Machine with three rotors
class RotorMachine:
    def __init__(self):
        self.alphabet = string.ascii_uppercase  # Only use uppercase for simplicity
        self.rotor1 = create_rotor()
        self.rotor2 = create_rotor()
        self.rotor3 = create_rotor()
        self.rotor_positions = [0, 0, 0]  # Initial positions for each rotor

    def rotate_rotors(self):
        self.rotor_positions[0] += 1
        if self.rotor_positions[0] >= len(self.alphabet):
            self.rotor_positions[0] = 0
            self.rotor_positions[1] += 1
            if self.rotor_positions[1] >= len(self.alphabet):
                self.rotor_positions[1] = 0
                self.rotor_positions[2] += 1
                if self.rotor_positions[2] >= len(self.alphabet):
                    self.rotor_positions[2] = 0

    def encrypt_char(self, char):
        index = self.alphabet.index(char)
        step1 = (index + self.rotor_positions[0]) % len(self.alphabet)
        char = self.rotor1[step1]
        step2 = (self.alphabet.index(char) + self.rotor_positions[1]) % len(self.alphabet)
        char = self.rotor2[step2]
        step3 = (self.alphabet.index(char) + self.rotor_positions[2]) % len(self.alphabet)
        return self.rotor3[step3]

    def decrypt_char(self, char):
        index = self.rotor3.index(char)
        step3 = (index - self.rotor_positions[2]) % len(self.alphabet)
        char = self.alphabet[step3]
        index = self.rotor2.index(char)
        step2 = (index - self.rotor_positions[1]) % len(self.alphabet)
        char = self.alphabet[step2]
        index = self.rotor1.index(char)
        step1 = (index - self.rotor_positions[0]) % len(self.alphabet)
        return self.alphabet[step1]

    def encrypt(self, text):
        encrypted_text = ''
        for char in text.upper():
            if char in self.alphabet:
                encrypted_char = self.encrypt_char(char)
                self.rotate_rotors()
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, text):
        decrypted_text = ''
        for char in text.upper():
            if char in self.alphabet:
                decrypted_char = self.decrypt_char(char)
                self.rotate_rotors()
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        return decrypted_text

# Example usage
if __name__ == "__main__":
    rotor_machine = RotorMachine()
    message = "HELLO WORLD"
    encrypted_rotor = rotor_machine.encrypt(message)
    decrypted_rotor = rotor_machine.decrypt(encrypted_rotor)

    print("Rotor Encrypted:", encrypted_rotor)
    print("Rotor Decrypted:", decrypted_rotor)

    # DES encryption
    key = get_random_bytes(8)  # DES key must be 8 bytes
    des_encrypted = des_encrypt(encrypted_rotor, key)
    des_decrypted = des_decrypt(des_encrypted, key)

    print("DES Encrypted (bytes):", des_encrypted)
    print("DES Decrypted (text):", des_decrypted)
