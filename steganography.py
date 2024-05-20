import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet
from stegano import lsb

# Function to load the encryption key


def load_key(key_path):
    with open(key_path, "rb") as key_file:
        key = key_file.read()
    return key

# Function to encrypt a ZIP file


def encrypt_zip(zip_file_path, key):
    cipher = Fernet(key)
    with open(zip_file_path, "rb") as file:
        zip_data = file.read()
    encrypted_zip_data = cipher.encrypt(zip_data)
    return encrypted_zip_data

# Function to hide encrypted ZIP file in an image


def hide_zip(image_path, encrypted_zip_data, output_image_path):
    secret_image = lsb.hide(image_path, encrypted_zip_data.decode('latin1'))
    secret_image.save(output_image_path)
    messagebox.showinfo("Success", f"Encrypted ZIP file hidden in {
                        output_image_path}")

# Function to decrypt a ZIP file


def decrypt_zip(encrypted_zip_data, key):
    cipher = Fernet(key)
    zip_data = cipher.decrypt(encrypted_zip_data)
    return zip_data

# Function to retrieve hidden encrypted ZIP file from an image


def retrieve_zip(image_path):
    hidden_message = lsb.reveal(image_path)
    encrypted_zip_data = hidden_message.encode('latin1')
    return encrypted_zip_data


def encrypt_and_hide():
    zip_file_path = filedialog.askopenfilename(
        title="Select the ZIP file to encrypt")
    if not zip_file_path:
        return  # User cancelled the file dialog

    key_path = filedialog.askopenfilename(title="Select the encryption key")
    if not key_path:
        return  # User cancelled the file dialog

    image_path = filedialog.askopenfilename(
        title="Select the image to hide the ZIP file in")
    if not image_path:
        return  # User cancelled the file dialog

    output_image_path = filedialog.asksaveasfilename(
        defaultextension=".png", title="Save the output image")
    if not output_image_path:
        return  # User cancelled the file dialog

    key = load_key(key_path)
    encrypted_zip_data = encrypt_zip(zip_file_path, key)
    hide_zip(image_path, encrypted_zip_data, output_image_path)


def retrieve_and_decrypt():
    image_path = filedialog.askopenfilename(
        title="Select the image with hidden data")
    if not image_path:
        return  # User cancelled the file dialog

    key_path = filedialog.askopenfilename(title="Select the encryption key")
    if not key_path:
        return  # User cancelled the file dialog

    output_zip_path = filedialog.asksaveasfilename(
        defaultextension=".zip", title="Save the retrieved ZIP file")
    if not output_zip_path:
        return  # User cancelled the file dialog

    key = load_key(key_path)
    retrieved_encrypted_zip_data = retrieve_zip(image_path)
    decrypted_zip_data = decrypt_zip(retrieved_encrypted_zip_data, key)

    with open(output_zip_path, "wb") as file:
        file.write(decrypted_zip_data)
    messagebox.showinfo(
        "Success", f"Retrieved and decrypted ZIP file saved as {output_zip_path}")


def create_ui():
    root = tk.Tk()
    root.title("Steganography")

    # Adding style to the UI
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=6, relief="flat",
                    background="#3EAAE1", foreground="white")
    style.map("TButton", background=[("active", "#338ACD")])

    # Creating notebook with tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Encryption tab
    encrypt_tab = ttk.Frame(notebook)
    notebook.add(encrypt_tab, text="Encrypt")

    ttk.Label(encrypt_tab, text="Select the ZIP file to encrypt:").pack(
        pady=(10, 5))
    ttk.Button(encrypt_tab, text="Browse", command=encrypt_and_hide).pack()

    # Decryption tab
    decrypt_tab = ttk.Frame(notebook)
    notebook.add(decrypt_tab, text="Decrypt")

    ttk.Label(decrypt_tab, text="Select the image with hidden data:").pack(
        pady=(10, 5))
    ttk.Button(decrypt_tab, text="Browse", command=retrieve_and_decrypt).pack()

    root.mainloop()


create_ui()
