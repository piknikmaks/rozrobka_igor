from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class MoneyDisplay(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._money = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Монети: 0")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")

        layout.addWidget(self.label)
    
    def set_money(self, value: int):
        self._money = value
        self.label.setText(f"Монети: {value}")

class ClickButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton("КЛІК")
        self.button.setFixedHeight(516)
        self.button.setStyleSheet("""
            QPushButton {
                background: none;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                font-size: 20px;
                border: 1px solid #bdbdbd;
            }
            QPushButton:pressed {
                background: #ebebeb;
                font-size: 20px;
                border: 1px solid #a8a8a8;
            }
        """)

        layout.addWidget(self.button)

        self.button.clicked.connect(self.clicked.emit)
