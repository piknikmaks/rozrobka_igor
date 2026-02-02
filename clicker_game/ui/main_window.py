from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.widgets import ClickButton, MoneyDisplay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.current_money = 0
        self.setWindowTitle("Clicker Game")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("assets/icon.png"))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        left_panel = QWidget()
        left_panel.setFixedWidth(500)
        
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)
        left_panel.setLayout(left_layout)
        left_panel.setStyleSheet("border-right: 2px solid #a8a8a8;")
        
        self.money_label = MoneyDisplay()
        self.click_button = ClickButton()
        
        left_layout.addWidget(self.money_label)
        left_layout.addWidget(self.click_button)
        
        self.click_button.clicked.connect(self.on_click)

        right_panel = QWidget()
        right_panel.setFixedWidth(298)
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)
        right_panel.setLayout(right_layout)
        
        right_panel.upgrade_label = QLabel("Апгрейди")
        right_panel.upgrade_label.setAlignment(Qt.AlignCenter)
        right_panel.upgrade_label.setStyleSheet("font-size: 18px")
        
        right_layout.addWidget(right_panel.upgrade_label)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
    
    def on_click(self):
        self.current_money += 1
        self.money_label.set_money(self.current_money)