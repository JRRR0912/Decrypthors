import string
import random
import itertools




class Rotor:
    def __init__(self, name, wiring, notch, initial_position=0):
        self.name = name
        self.wiring = wiring
        self.notch = notch
        self.position = initial_position
        self.initial_position = initial_position

    def rotate(self):
        # Advance rotor position and check if it reached the notch
        is_at_notch = self.position == self.notch
        self.position = (self.position + 1) % 26
        return is_at_notch

    def forward(self, letter):
        # Pass letter through the rotor forwards
        letter_index = (string.ascii_uppercase.index(letter) + self.position) % 26
        mapped_letter = self.wiring[letter_index]
        output_index = (string.ascii_uppercase.index(mapped_letter) - self.position) % 26
        return string.ascii_uppercase[output_index]

    def backward(self, letter):
        # Shift the input letter index by rotor position
        letter_index = (string.ascii_uppercase.index(letter) + self.position) % 26
        # Apply inverse wiring mapping
        mapped_index = self.wiring.index(string.ascii_uppercase[letter_index])
        # Shift back by rotor position
        output_index = (mapped_index - self.position) % 26
        # Return the output letter
        return string.ascii_uppercase[output_index]

    def reset(self):
        # Reset rotor to initial position
        self.position = self.initial_position


class Plugboard:
    def __init__(self, swaps):
        self.swaps = {**swaps, **{v: k for k, v in swaps.items()}}  # Ensure symmetrical mappings

    def substitute(self, letter):
        # Substitute letter with swap if it exists in plugboard
        return self.swaps.get(letter, letter)


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, letter):
        # Reflect letter through the reflector wiring
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

    def process_text(self, text):
        result_text = []
        for letter in text.upper():
            if letter in string.ascii_uppercase:
                self.step_rotors()  # Rotate rotors before processing each letter
                letter = self.plugboard.substitute(letter)

                # Forward pass through rotors
                for rotor in self.rotors:
                    letter = rotor.forward(letter)

                # Pass through reflector
                letter = self.reflector.reflect(letter)

                # Backward pass through rotors
                for rotor in reversed(self.rotors):
                    letter = rotor.backward(letter)

                # Final plugboard substitution
                letter = self.plugboard.substitute(letter)
                result_text.append(letter)
            else:
                result_text.append(letter)
        return ''.join(result_text)

    def encrypt(self, text):
        # Reset rotors before starting encryption
        for rotor in self.rotors:
            rotor.reset()
        return self.process_text(text)

    def decrypt(self, text):
        # Reset rotors before starting decryption
        for rotor in self.rotors:
            rotor.reset()
        return self.process_text(text)


# Example usage
if __name__ == "__main__":
    # Example usage:
    rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)  # Notch at 'R'
    rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)  # Notch at 'F'
    rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)  # Notch at 'W'
    plugboard = Plugboard({'A': 'J', 'B': 'G', 'C': 'D'})
    reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')

    enigma_machine = EnigmaMachine([rotor1, rotor2, rotor3], plugboard, reflector)

    # Task 1 and 2
    text = ["HELLO", "HOPE", "NEW YEAR"]
    for word in text:
        encrypted_rotor = enigma_machine.encrypt(word)
        print(f'Encrypted using Rotor Machine {word}: {encrypted_rotor}')

        # encrypted_DES =
        # print(f'Encrypted using DES {word}: {encrypted_DES}')

        decrypted_rotor = enigma_machine.decrypt(encrypted_rotor)
        print(f'Decrypted back using Rotor Machine: {decrypted_rotor}')
        # decrypted_DES =
        # print(f'Decrypted back using Rotor Machine: {decrypted_DES}')




