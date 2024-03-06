import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


class DSSSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSS Digital Signature App")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.key_size_entry = QLineEdit()
        self.key_size_entry.setPlaceholderText("Key Size (Default: 1024)")
        self.key_size_entry.setFixedHeight(40)
        layout.addWidget(self.key_size_entry)

        self.message_entry = QLineEdit()
        self.message_entry.setPlaceholderText("Message to Sign")
        self.message_entry.setFixedHeight(40)
        layout.addWidget(self.message_entry)

        self.generate_button = QPushButton("Generate Keys Sign")
        self.generate_button.clicked.connect(self.generate_keys_and_sign)
        layout.addWidget(self.generate_button)

        self.signature_entry = QLineEdit()
        self.signature_entry.setPlaceholderText("DSS Signature")
        self.signature_entry.setFixedHeight(40) 
        layout.addWidget(self.signature_entry)

        self.verify_button = QPushButton("Verify Signature")
        self.verify_button.clicked.connect(self.verify_signature)
        layout.addWidget(self.verify_button)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_values)
        layout.addWidget(self.update_button)

        self.public_key_label = QTextEdit()
        self.public_key_label.setReadOnly(True)
        self.public_key_label.setFixedHeight(300)
        layout.addWidget(self.public_key_label)

        self.private_key_label = QLabel()
        layout.addWidget(self.private_key_label)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def generate_keys_and_sign(self):
        key_size_str = self.key_size_entry.text()
        key_size = int(key_size_str) if key_size_str.isdigit() else 1024

        key = DSA.generate(key_size)

        public_key_info = f"Public Key Parameters:\n\ny: {key.y}\ng: {key.g}\np: {key.p}\nq: {key.q}\n"
        self.public_key_label.setText(public_key_info)

        private_key_info = f"Private Key Parameters:\n\nx: {key.x}\n"
        self.private_key_label.setText(private_key_info)

        message = self.message_entry.text().encode('utf-8')

        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(SHA256.new(message))

        self.signature_entry.setText(signature.hex())

        self.status_label.setText("Message Signed Successfully!")

        self.key = key
        self.signature = signature
        self.message = message

    def verify_signature(self):
        if not hasattr(self, 'key') or not hasattr(self, 'signature') or not hasattr(self, 'message'):
            QMessageBox.critical(self, "Error", "No signature to verify.")
            return

        verifier = DSS.new(self.key, 'fips-186-3')
        h = SHA256.new(self.message)

        try:
            verifier.verify(h, self.signature)
            QMessageBox.information(self, "Verification", "Signature is valid.")
        except ValueError:
            QMessageBox.critical(self, "Verification", "Signature is invalid or data has been changed.")

    def update_values(self):
        if hasattr(self, 'message'):
            self.message = self.message_entry.text().encode('utf-8')
        if hasattr(self, 'signature'):
            self.signature = bytes.fromhex(self.signature_entry.text())
        if hasattr(self, 'key'):
            key = self.key
            public_key_info = f"Public Key Parameters:\n\ny: {key.y}\ng: {key.g}\np: {key.p}\nq: {key.q}\n"
            self.public_key_label.setPlainText(public_key_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DSSSignatureApp()
    window.show()
    sys.exit(app.exec_())
