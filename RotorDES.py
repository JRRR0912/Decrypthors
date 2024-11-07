import string
import random
import itertools

subkeys = [
    '01111111', '10111111', '11011111', '11101111',
    '11110111', '11111011', '11111101', '11111110',
    '10101010', '01010101', '10100101', '01011010',
    '00001111', '00110011', '11001100', '11110000'
]


class DES:

    # ***
    # with this method, the input plaintext
    # goes through the initial permutation
    # ***
    def FirstPermutate(text, key):
        perm = list()
        wordSplit = text.split()
        for word in wordSplit:
            charSplit = list(word)
            permutations = list(itertools.permutations(charSplit))
            permPos = random.randrange(0, len(permutations))
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

class Rotor:
    def __init__(self, name, wiring, notch):
        self.name = name
        self.wiring = wiring
        self.notch = notch  # Indicates the position that triggers the next rotor to advance
        self.position = 0

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch

    def encrypt(self, letter):
        index = (string.ascii_uppercase.index(letter) + self.position) % 26
        letter = self.wiring[index]
        index = (string.ascii_uppercase.index(letter) - self.position) % 26
        return string.ascii_uppercase[index]

    def decrypt(self, letter):
        index = (string.ascii_uppercase.index(letter) + self.position) % 26
        letter = string.ascii_uppercase[self.wiring.index(letter)]
        index = (string.ascii_uppercase.index(letter) - self.position) % 26
        return string.ascii_uppercase[index]

class Plugboard:
    def __init__(self, swaps):
        self.swaps = swaps

    def substitute(self, letter):
        return self.swaps.get(letter, letter)

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

    def step_rotors(self):
        rotate_next = True
        for rotor in self.rotors:
            if rotate_next:
                rotate_next = rotor.rotate()
            else:
                break

    def encrypt(self, text):
        encrypted_text = []
        for letter in text.upper():
            if letter in string.ascii_uppercase:
                self.step_rotors()  # Rotate rotors before encrypting each letter
                letter = self.plugboard.substitute(letter)
                for rotor in self.rotors:
                    letter = rotor.encrypt(letter)
                letter = self.reflector.reflect(letter)
                for rotor in reversed(self.rotors):
                    letter = rotor.decrypt(letter)
                encrypted_text.append(letter)
            else:
                encrypted_text.append(letter)
        return ''.join(encrypted_text)

    def decrypt(self, text):
        decrypted_text = []
        for letter in text.upper():
            if letter in string.ascii_uppercase:
                self.step_rotors()  # Rotate rotors before decrypting each letter
                for rotor in reversed(self.rotors):
                    letter = rotor.decrypt(letter)
                letter = self.reflector.reflect(letter)
                for rotor in self.rotors:
                    letter = rotor.encrypt(letter)
                decrypted_text.append(letter)
            else:
                decrypted_text.append(letter)
        return ''.join(decrypted_text)


# Example usage
if __name__ == "__main__":
    # Example usage:
    rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)  # Notch at 'R'
    rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)  # Notch at 'F'
    rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)  # Notch at 'W'
    plugboard = Plugboard({'A': 'J', 'B': 'G', 'C': 'D'})
    reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')

    enigma_machine = EnigmaMachine([rotor1, rotor2, rotor3], plugboard, reflector)

    text = 'HELLO WORLD*&%*&%^&$%^#'
    encrypted_text = enigma_machine.encrypt(text)
    print(encrypted_text)  # Output: GUR PENML XRL




