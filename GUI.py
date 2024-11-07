import tkinter as tk
from Rotor import Rotor, Plugboard, Reflector, EnigmaMachine

class App:
    def __init__(self, master):
        self.master = master
        master.title("Enigma Machine Simulator")

        # Input label and text entry
        self.label_input = tk.Label(master, text="Enter your text:")
        self.label_input.grid(row=0, column=0, padx=10, pady=10)

        self.text_input = tk.Entry(master, width=50)
        self.text_input.grid(row=0, column=1, padx=10, pady=10)

        # Buttons for Encrypt and Decrypt
        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=1, column=0, padx=10, pady=10)

        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(row=1, column=1, padx=10, pady=10)

        # Output label and output display
        self.label_output = tk.Label(master, text="Result:")
        self.label_output.grid(row=2, column=0, padx=10, pady=10)

        self.text_output = tk.Entry(master, width=50)
        self.text_output.grid(row=2, column=1, padx=10, pady=10)

        # Set up the Enigma machine
        self.setup_enigma_machine()

    def setup_enigma_machine(self):
        # Define rotors, plugboard, and reflector here:
        rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)  # Notch at 'R'
        rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)  # Notch at 'F'
        rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)  # Notch at 'W'
        plugboard_config = {'A': 'J', 'B': 'G', 'C': 'D'}  # Example plugboard configuration
        plugboard = Plugboard(plugboard_config)
        reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')

        self.enigma_machine = EnigmaMachine([rotor1, rotor2, rotor3], plugboard, reflector)

    def encrypt(self):
        input_text = self.text_input.get().strip()
        encrypted_text = self.enigma_machine.encrypt(input_text)
        self.text_output.delete(0, tk.END)
        self.text_output.insert(0, encrypted_text)

    def decrypt(self):
        input_text = self.text_input.get().strip()
        decrypted_text = self.enigma_machine.decrypt(input_text)
        self.text_output.delete(0, tk.END)
        self.text_output.insert(0, decrypted_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x150")  # Setting a suitable size for the window
    app = App(root)
    root.mainloop()
