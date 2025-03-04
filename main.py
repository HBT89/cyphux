import tkinter as tk
from tkinter import messagebox
import json
import random
import string
import os

# File to store the committed cipher
CIPHER_FILE = "cipher.json"

def generate_cipher():
    """Generate a new random cipher table."""
    leet_chars = ["@4^", "B8#", "C(=", "D|)", "3€=", "F7}", "G6&", "H#4", "1!|", "J_)", "KX<", "L1_", "M^^", "|\|7", "0o*", "P9¶", "Q&9", "R2®", "S5$", "T+7", "U(_)", "V\/", "W\\/\\/", "X}{", "Y¥?", "Z2%"]
    random.shuffle(leet_chars)
    return {char: leet_chars[i] for i, char in enumerate(string.ascii_uppercase)}

def load_committed_cipher():
    """Load the committed cipher if it exists."""
    if os.path.exists(CIPHER_FILE):
        with open(CIPHER_FILE, "r") as file:
            return json.load(file)
    return None

def save_committed_cipher(cipher):
    """Save the committed cipher to a file."""
    with open(CIPHER_FILE, "w") as file:
        json.dump(cipher, file)

def commit_cipher():
    """Lock in the currently displayed cipher."""
    global committed_cipher
    committed_cipher = current_cipher.copy()
    save_committed_cipher(committed_cipher)
    messagebox.showinfo("Success", "Cipher has been committed and will persist.")
    update_display(committed_cipher)

def encrypt_word():
    """Encrypt user input using the committed cipher."""
    if committed_cipher is None:
        messagebox.showerror("Error", "You must commit a cipher before using it.")
        return
    word = entry_word.get().upper()
    encrypted_word = "".join(committed_cipher.get(char, char) for char in word)
    output_var.set(encrypted_word)

def update_display(cipher):
    """Update the UI with the provided cipher."""
    for char, box in letter_boxes.items():
        box.delete(0, tk.END)
        box.insert(0, cipher[char])
        if committed_cipher:
            box.config(state='disabled')

def regenerate_cipher():
    """Generate a new cipher and update the display."""
    global current_cipher
    if committed_cipher:
        messagebox.showerror("Error", "You have already committed a cipher. Reset to generate a new one.")
        return
    current_cipher = generate_cipher()
    update_display(current_cipher)

# Load committed cipher if exists
committed_cipher = load_committed_cipher()
current_cipher = committed_cipher if committed_cipher else generate_cipher()

# Create GUI
root = tk.Tk()
root.title("Password Cypher Tool")
root.geometry("600x400")

letter_boxes = {}
tk.Label(root, text="Letter Mapping Table").pack()
frame = tk.Frame(root)
frame.pack()

for i, letter in enumerate(string.ascii_uppercase):
    tk.Label(frame, text=letter).grid(row=0, column=i)
    entry = tk.Entry(frame, width=5, justify='center')
    entry.grid(row=1, column=i)
    letter_boxes[letter] = entry

update_display(current_cipher)

generate_btn = tk.Button(root, text="Generate Cipher", command=regenerate_cipher)
generate_btn.pack()
commit_btn = tk.Button(root, text="Commit Cipher", command=commit_cipher)
commit_btn.pack()

tk.Label(root, text="Enter Word to Encrypt:").pack()
entry_word = tk.Entry(root)
entry_word.pack()

encrypt_btn = tk.Button(root, text="Encrypt", command=encrypt_word)
encrypt_btn.pack()
output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, state='readonly')
output_entry.pack()

tk.Button(root, text="Copy", command=lambda: root.clipboard_append(output_var.get())).pack()

root.mainloop()
