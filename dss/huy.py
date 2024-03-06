import tkinter as tk
from tkinter import messagebox
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


class DSSSignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSS Digital Signature App")

        self.create_widgets()

    def create_widgets(self):
        # Key size
        tk.Label(self.root, text="Key Size:").grid(row=0, column=0, sticky="w")
        self.key_size_entry = tk.Entry(self.root, width=50)
        self.key_size_entry.grid(row=0, column=1, padx=5, pady=5)
        self.key_size_entry.insert(tk.END, "1024")

        # Message to sign
        tk.Label(self.root, text="Message to Sign:").grid(row=1, column=0, sticky="w")
        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to generate keys and sign
        self.sign_button = tk.Button(self.root, text="Generate Keys & Sign", command=self.generate_keys_and_sign)
        self.sign_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Public key parameters
        tk.Label(self.root, text="Public Key Parameters:").grid(row=3, column=0, sticky="w")
        self.public_key_text = tk.Text(self.root, width=50, height=4)
        self.public_key_text.grid(row=3, column=1, padx=5, pady=5)

        # Private key parameters
        tk.Label(self.root, text="Private Key Parameters:").grid(row=4, column=0, sticky="w")
        self.private_key_text = tk.Text(self.root, width=50, height=4)
        self.private_key_text.grid(row=4, column=1, padx=5, pady=5)

        # DSS Signature
        tk.Label(self.root, text="DSS Signature:").grid(row=5, column=0, sticky="w")
        self.signature_text = tk.Text(self.root, width=50, height=4)
        self.signature_text.grid(row=5, column=1, padx=5, pady=5)

        # Status
        tk.Label(self.root, text="Status:").grid(row=6, column=0, sticky="w")
        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=6, column=1, padx=5, pady=5)

    def generate_keys_and_sign(self):
        # Get key size
        key_size_str = self.key_size_entry.get()
        if key_size_str.isdigit():
            key_size = int(key_size_str)
        else:
            key_size = 1024

        # Generate key pair
        key = DSA.generate(key_size)

        # Display public key parameters
        public_key_info = "y: {}\ng: {}\np: {}\nq: {}\n".format(
            key.y, key.g, key.p, key.q)
        self.public_key_text.delete('1.0', tk.END)
        self.public_key_text.insert(tk.END, public_key_info)

        # Display private key parameters
        private_key_info = "x: {}\n".format(key.x)
        self.private_key_text.delete('1.0', tk.END)
        self.private_key_text.insert(tk.END, private_key_info)

        # Get message to sign
        message = self.message_entry.get().encode('utf-8')

        # Sign data
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(SHA256.new(message))

        # Display signature
        self.signature_text.delete('1.0', tk.END)
        self.signature_text.insert(tk.END, signature.hex())

        # Display status
        self.status_label.config(text="Message Signed Successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DSSSignatureApp(root)
    root.mainloop()