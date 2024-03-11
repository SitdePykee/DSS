import sys
from sympy import isprime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5 import QtGui
import hashlib


class DigitalSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signature Calculation")
        self.setWindowIcon(QtGui.QIcon('decryption.png'))
        self.setGeometry(100, 100, 700, 500)
        self.initUI()

        self.p = None
        self.q = None
        self.g = None
        self.a = None
        self.k = None
        self.message_hash = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.delta = None
        self.e1 = None
        self.e2 = None

    def initUI(self):
        layout = QVBoxLayout()
        self.p_entry = QLineEdit()
        self.p_entry.setPlaceholderText("Enter prime number p (512 bits)")
        layout.addWidget(self.p_entry)

        self.q_entry = QLineEdit()
        self.q_entry.setPlaceholderText("Enter prime number q (160 bits)")
        layout.addWidget(self.q_entry)

        self.g_entry = QLineEdit()
        self.g_entry.setPlaceholderText("Enter g (a prime number in Zp*)")
        layout.addWidget(self.g_entry)

        self.a_entry = QLineEdit()
        self.a_entry.setPlaceholderText("Enter secret key a")
        layout.addWidget(self.a_entry)

        self.k_entry = QLineEdit()
        self.k_entry.setPlaceholderText("Enter random number k (1 <= k <= q - 1)")
        layout.addWidget(self.k_entry)

        self.message_entry = QLineEdit()
        self.message_entry.setPlaceholderText("Enter message")
        layout.addWidget(self.message_entry)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_signature)
        layout.addWidget(self.calculate_button)

        self.result_display = QTextEdit()
        layout.addWidget(self.result_display)

        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.verify_signature)
        layout.addWidget(self.verify_button)

        self.verify_status_label = QLabel("")
        layout.addWidget(self.verify_status_label)

        self.setLayout(layout)

    def calculate_signature(self):
        try:
            self.p = int(self.p_entry.text())
            self.q = int(self.q_entry.text())
            self.g = int(self.g_entry.text())
            self.a = int(self.a_entry.text())
            self.k = int(self.k_entry.text())
            message = self.message_entry.text().encode('utf-8')
            self.message_hash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')

            if not (isprime(self.p) and isprime(self.q)):
                raise ValueError("Error, p and q must be prime numbers")    # điều kiện p,q là số nguyên tố

            if not ((self.p-1) % self.q == 0):
                raise ValueError("Error, (p-1) is not divisible by q.")

            if not (1 <= self.k <= self.q - 1):
                raise ValueError("Error, k must be in the range 1 <= k <= q - 1")

            self.alpha = pow(self.g, int((self.p - 1) / self.q)) % self.p
            self.beta = pow(self.alpha, self.a, self.p)
            self.gamma = pow(self.alpha, self.k, self.p) % self.q
            self.delta = ((self.message_hash + self.a * self.gamma) * pow(self.k, -1, self.q)) % self.q
            self.e1 = self.message_hash * pow(self.delta, -1, self.q) % self.q
            self.e2 = self.gamma * pow(self.delta, -1, self.q) % self.q

            result_text = f"e1: {self.e1}\n" \
                          f"e2: {self.e2}\n" \
                          f"alpha: {self.alpha}\n" \
                          f"beta: {self.beta}\n" \
                          f"gamma: {self.gamma}\n" \
                          f"delta: {self.delta}\n" \
                          f"message hash: {self.message_hash}\n" \
                          f"=> Pair of signatures ({self.gamma},{self.delta})"
            self.result_display.setPlainText(result_text)

        except ValueError as e:
            self.result_display.setPlainText(str(e))
            return

    def verify_signature(self):
        try:
            signature_check = (pow(self.alpha, self.e1) * pow(self.beta, self.e2)) % self.p % self.q
            if signature_check == self.gamma:
                signature_text_true = f"-((alpha^e1 * beta^e2) mod p) mod q = {signature_check} = gamma " \
                                      f"\n-Ver({self.message_hash},{self.gamma},{self.delta}) = TRUE" \
                                      f"\n--->Verify valid signature"
                self.verify_status_label.setText(signature_text_true)
            else:
                signature_text_false = f"-((alpha^e1 * beta^e2) mod p) mod q = {signature_check} != gamma " \
                                       f"\n-Ver({self.message_hash},{self.gamma},{self.delta}) = FALSE" \
                                       f"\n--->Verify invalid signature"
                self.verify_status_label.setText(signature_text_false)
        except ValueError:
            self.verify_status_label.setText("Invalid input")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalSignatureApp()
    window.show()
    sys.exit(app.exec_())
