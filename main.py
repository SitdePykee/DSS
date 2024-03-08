import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit

class DigitalSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signature Calculation")
        self.setGeometry(100, 100, 400, 400)  # Increased height to accommodate additional components
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.p_entry = QLineEdit()
        self.p_entry.setPlaceholderText("Enter prime number p (512 bits)")
        layout.addWidget(self.p_entry)

        self.q_entry = QLineEdit()
        self.q_entry.setPlaceholderText("Enter prime number q (160 bits)")
        layout.addWidget(self.q_entry)

        self.alpha_entry = QLineEdit()
        self.alpha_entry.setPlaceholderText("Enter alpha (in Zp*)")
        layout.addWidget(self.alpha_entry)

        self.a_entry = QLineEdit()
        self.a_entry.setPlaceholderText("Enter secret key a")
        layout.addWidget(self.a_entry)

        self.k_entry = QLineEdit()
        self.k_entry.setPlaceholderText("Enter random number k (1 <= k <= q - 1)")
        layout.addWidget(self.k_entry)

        self.x_entry = QLineEdit()
        self.x_entry.setPlaceholderText("Enter message")
        layout.addWidget(self.x_entry)

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
            p = int(self.p_entry.text())
            q = int(self.q_entry.text())
            alpha = int(self.alpha_entry.text())
            a = int(self.a_entry.text())
            k = int(self.k_entry.text())
            x = int(self.x_entry.text())

            if not (1 <= k <= q - 1):
                raise ValueError("k must be in the range 1 <= k <= q - 1")

            beta = pow(alpha, a, p)
            gamma = pow(alpha, k, p) % q
            delta = ((x + a * gamma) * pow(k, -1, q)) % q
            e1 = x * pow(delta, -1, q) % q
            e2 = gamma * pow(delta, -1, q) % q

            signature_text = f"e1: {e1}\n" \
                             f"e2: {e2}\n" \
                             f"beta: {beta}\n" \
                             f"gamma: {gamma}\n" \
                             f"delta: {delta}\n" \
                             f"=> Pair of signatures ({gamma},{delta})"
            self.result_display.setPlainText(signature_text)

        except ValueError:
            self.result_display.setPlainText("Invalid input")
            return

    def verify_signature(self):
        try:
            p = int(self.p_entry.text())
            q = int(self.q_entry.text())
            alpha = int(self.alpha_entry.text())
            a = int(self.a_entry.text())
            k = int(self.k_entry.text())
            x = int(self.x_entry.text())

            beta = pow(alpha, a, p)
            gamma = pow(alpha, k, p) % q
            delta = ((x + a * gamma) * pow(k, -1, q)) % q
            e1 = x * pow(delta, -1, q) % q
            e2 = gamma * pow(delta, -1, q) % q

            if (pow(alpha, e1) * pow(beta, e2)) % p % q == gamma:
                self.verify_status_label.setText("Valid" )
            else:
                self.verify_status_label.setText("Invalid")

        except ValueError:
            self.verify_status_label.setText("Invalid input")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalSignatureApp()
    window.show()
    sys.exit(app.exec_())