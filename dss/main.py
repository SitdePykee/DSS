import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit

class DigitalSignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signature Calculation")
        self.setGeometry(100, 100, 400, 300)
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

            gamma = (pow(alpha, k, p) % q)
            delta = ((x + a * gamma) * pow(k, -1, q)) % q
            e1 = (x * pow(delta, -1, q)) % q
            e2 = (gamma * pow(delta, -1, q)) % q

            result_text = f"e1: {e1}\n" \
                          f"e2: {e2}\n" \
                          f"gamma: {gamma}\n" \
                          f"delta: {delta}"
            self.result_display.setPlainText(result_text)

        except ValueError as e:
            self.result_display.setPlainText(str(e))
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalSignatureApp()
    window.show()
    sys.exit(app.exec_())
