import string
import random

class Rotor:
    def __init__(self, name, wiring):
        self.name = name
        self.wiring = wiring
        self.position = 0

    def encrypt(self, letter):
        index = string.ascii_uppercase.index(letter)
        return self.wiring[(index + self.position) % 26]

    def decrypt(self, letter):
        index = self.wiring.index(letter)
        return string.ascii_uppercase[(index - self.position) % 26]

class Plugboard:
    def __init__(self, swaps):
        self.swaps = swaps

    def substitute(self, letter):
        if letter in self.swaps:
            return self.swaps[letter]
        return letter

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, letter):
        index = string.ascii_uppercase.index(letter)
        return self.wiring[index]

class EnigmaMachine:
    def __init__(self, rotors, plugboard, reflector):
        self.rotors = rotors
        self.plugboard = plugboard
        self.reflector = reflector

    def encrypt(self, text):
        encrypted_text = []
        for letter in text.upper():
            if letter in string.ascii_uppercase:
                letter = self.plugboard.substitute(letter)
                for rotor in self.rotors:
                    letter = rotor.encrypt(letter)
                letter = self.reflector.reflect(letter)
                for rotor in reversed(self.rotors):
                    letter = rotor.decrypt(letter)
                encrypted_text.append(letter)
            else:
                encrypted_text.append(letter)  # Append non-alphabetic characters unchanged
        return ''.join(encrypted_text)

    def decrypt(self, text):
        decrypted_text = []
        for letter in text.upper():
            if letter in string.ascii_uppercase:
                for rotor in reversed(self.rotors):
                    letter = rotor.encrypt(letter)
                letter = self.reflector.reflect(letter)
                for rotor in self.rotors:
                    letter = rotor.decrypt(letter)
                decrypted_text.append(letter)
            else:
                decrypted_text.append(letter)  # Append non-alphabetic characters unchanged
        return ''.join(decrypted_text)

# Example usage
if __name__ == "__main__":
    rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ')
    rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE')
    rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO')

    plugboard = Plugboard({'A': 'J', 'B': 'G', 'C': 'D'})
    reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')

    enigma_machine = EnigmaMachine([rotor1, rotor2, rotor3], plugboard, reflector)

    text = 'HELLO WORLD'
    encrypted_text = enigma_machine.encrypt(text)
    print(encrypted_text)  # Example output
