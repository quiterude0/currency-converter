import os
import sys
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QFrame)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

# Load environment variables
load_dotenv()

class CurrencyConverter:
    def __init__(self):
        self.api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please check your .env file.")
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD"
        self.currencies = self.get_currencies()

    def get_currencies(self):
        response = requests.get(self.base_url)
        data = response.json()
        if data['result'] == 'success':
            return sorted(list(data['conversion_rates'].keys()))
        else:
            raise Exception("Failed to fetch currencies")

    def convert(self, amount, from_currency, to_currency):
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url)
        data = response.json()
        
        if data['result'] == 'success':
            return data['conversion_result']
        else:
            raise Exception("Currency conversion failed")

class CurrencyConverterApp(QMainWindow):
    def __init__(self, converter):
        super().__init__()
        self.converter = converter
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Currency Converter')
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 16px;
            }
            QLineEdit, QComboBox {
                background-color: #34495E;
                border: 2px solid #3498DB;
                border-radius: 5px;
                color: #ECF0F1;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;
                color: #ECF0F1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            #resultFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Amount input
        amount_layout = QHBoxLayout()
        self.amount_label = QLabel('Amount:')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Enter amount')
        amount_layout.addWidget(self.amount_label)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)

        # From currency
        from_layout = QHBoxLayout()
        self.from_label = QLabel('From:')
        self.from_combo = QComboBox()
        self.from_combo.addItems(self.converter.currencies)
        self.from_combo.setCurrentText('USD')
        from_layout.addWidget(self.from_label)
        from_layout.addWidget(self.from_combo)
        layout.addLayout(from_layout)

        # To currency
        to_layout = QHBoxLayout()
        self.to_label = QLabel('To:')
        self.to_combo = QComboBox()
        self.to_combo.addItems(self.converter.currencies)
        self.to_combo.setCurrentText('EUR')
        to_layout.addWidget(self.to_label)
        to_layout.addWidget(self.to_combo)
        layout.addLayout(to_layout)

        # Convert button
        self.convert_btn = QPushButton('Convert')
        self.convert_btn.clicked.connect(self.perform_conversion)
        layout.addWidget(self.convert_btn)

        # Result frame
        self.result_frame = QFrame()
        self.result_frame.setObjectName('resultFrame')
        result_layout = QVBoxLayout(self.result_frame)
        self.result_label = QLabel('Result will appear here')
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        result_layout.addWidget(self.result_label)
        layout.addWidget(self.result_frame)

        layout.addStretch()

    def perform_conversion(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_combo.currentText()
            to_currency = self.to_combo.currentText()

            result = self.converter.convert(amount, from_currency, to_currency)
            
            # Animate the result
            self.result_label.setText(f"{amount:.2f} {from_currency}\n=\n{result:.2f} {to_currency}")
            self.animate_result()
        except ValueError:
            self.result_label.setText("Please enter a valid amount")
        except Exception as e:
            self.result_label.setText(str(e))

    def animate_result(self):
        animation = QPropertyAnimation(self.result_frame, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.result_frame.geometry())
        animation.setEndValue(self.result_frame.geometry().adjusted(-5, -5, 5, 5))
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()

def main():
    try:
        app = QApplication(sys.argv)
        converter = CurrencyConverter()
        ex = CurrencyConverterApp(converter)
        ex.show()
        sys.exit(app.exec())
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure you have a .env file with EXCHANGE_RATE_API_KEY set.")

if __name__ == '__main__':
    main()