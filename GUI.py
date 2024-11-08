import string
import tkinter as tk
from tkinter import ttk, messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# Fixed 64-bit (8-byte) key and IV for DES
key = b'8bytekey'  # 8 bytes = 64 bits
iv = b'8byteiv!'  # 8 bytes = 64 bits

# Classes for Rotor Machine, Plugboard, Reflector, and EnigmaMachine (as in previous code)
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

# DES encryption and decryption functions
def des_encrypt(plaintext):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext

def des_decrypt(ciphertext):
    decipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_padded_text = decipher.decrypt(ciphertext)
    decrypted_text = unpad(decrypted_padded_text, DES.block_size)
    return decrypted_text.decode('utf-8')


# Initialize the Enigma Machine components
rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 17)
rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 5)
rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 22)
plugboard = Plugboard({'A': 'J', 'B': 'G', 'C': 'D'})
reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')

enigma_machine = EnigmaMachine([rotor1, rotor2, rotor3], plugboard, reflector)


# Function to handle encryption based on selected checkboxes
def on_encrypt():
    plaintext = text_input.get("1.0", tk.END).strip()
    if not plaintext:
        messagebox.showwarning("Input Required", "Please enter text to encrypt.")
        return

    if des_var.get() and rotor_var.get():
        # Hybrid encryption: Rotor Machine first, then DES
        encrypted_rotor = enigma_machine.encrypt(plaintext)
        encrypted_DES = des_encrypt(plaintext)
        encrypted_hybrid = des_encrypt(encrypted_rotor)

        # Display in all output boxes
        rotor_output.delete("1.0", tk.END)
        rotor_output.insert(tk.END, encrypted_rotor)

        des_output.delete("1.0", tk.END)
        des_output.insert(tk.END, encrypted_DES.hex())

        hybrid_output.delete("1.0", tk.END)
        hybrid_output.insert(tk.END, encrypted_hybrid.hex())
    elif rotor_var.get():
        # Only Rotor Machine encryption
        encrypted_rotor = enigma_machine.encrypt(plaintext)
        rotor_output.delete("1.0", tk.END)
        rotor_output.insert(tk.END, encrypted_rotor)
        des_output.delete("1.0", tk.END)
        hybrid_output.delete("1.0", tk.END)
    elif des_var.get():
        # Only DES encryption
        encrypted_DES = des_encrypt(plaintext)
        rotor_output.delete("1.0", tk.END)
        des_output.delete("1.0", tk.END)
        des_output.insert(tk.END, encrypted_DES.hex())
        hybrid_output.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Selection Required", "Please select at least one encryption method.")


# Function to handle decryption based on selected checkboxes
def on_decrypt():
    ciphertext = text_input.get("1.0", tk.END).strip()
    if not ciphertext:
        messagebox.showwarning("Input Required", "Please enter text to decrypt.")
        return

    try:
        if des_var.get() and rotor_var.get():
            # Hybrid decryption: DES first, then Rotor Machine
            encrypted_DES_bytes = bytes.fromhex(ciphertext)
            decrypted_DES = des_decrypt(encrypted_DES_bytes)
            decrypted_rotor = enigma_machine.decrypt(decrypted_DES)
            result = decrypted_rotor

            # Display in all output boxes
            rotor_output.delete("1.0", tk.END)
            rotor_output.insert(tk.END, decrypted_rotor)

            des_output.delete("1.0", tk.END)
            des_output.insert(tk.END, decrypted_DES)

            hybrid_output.delete("1.0", tk.END)
            hybrid_output.insert(tk.END, decrypted_rotor)
        elif rotor_var.get():
            # Only Rotor Machine decryption
            result = enigma_machine.decrypt(ciphertext)
            rotor_output.delete("1.0", tk.END)
            rotor_output.insert(tk.END, result)
            des_output.delete("1.0", tk.END)
            hybrid_output.delete("1.0", tk.END)
        elif des_var.get():
            # Only DES decryption
            encrypted_DES_bytes = bytes.fromhex(ciphertext)
            result = des_decrypt(encrypted_DES_bytes)
            rotor_output.delete("1.0", tk.END)
            des_output.delete("1.0", tk.END)
            des_output.insert(tk.END, result)
            hybrid_output.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Selection Required", "Please select at least one decryption method.")
            return
    except Exception as e:
        messagebox.showerror("Decryption Error", f"An error occurred during decryption:\n{e}")


# Set up the main application window
root = tk.Tk()
root.title("Encryption and Decryption GUI")

# Input Text
ttk.Label(root, text="Input Text:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
text_input = tk.Text(root, height=5, width=50)
text_input.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Checkboxes for DES and Rotor Machine selection
des_var = tk.BooleanVar()
rotor_var = tk.BooleanVar()

ttk.Checkbutton(root, text="DES", variable=des_var).grid(row=2, column=0, padx=5, pady=5, sticky='w')
ttk.Checkbutton(root, text="Rotor Machine", variable=rotor_var).grid(row=2, column=1, padx=5, pady=5, sticky='w')

# Encrypt and Decrypt Buttons
encrypt_button = ttk.Button(root, text="Encrypt", command=on_encrypt)
encrypt_button.grid(row=3, column=0, padx=5, pady=5)

decrypt_button = ttk.Button(root, text="Decrypt", command=on_decrypt)
decrypt_button.grid(row=3, column=1, padx=5, pady=5)

# Rotor Machine Output
ttk.Label(root, text="Rotor Machine Output:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
rotor_output = tk.Text(root, height=5, width=50)
rotor_output.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# DES Output
ttk.Label(root, text="DES Output (Hexadecimal):").grid(row=6, column=0, padx=5, pady=5, sticky='w')
des_output = tk.Text(root, height=5, width=50)
des_output.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

# Hybrid Output
ttk.Label(root, text="Hybrid Output:").grid(row=8, column=0, padx=5, pady=5, sticky='w')
hybrid_output = tk.Text(root, height=5, width=50)
hybrid_output.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()
