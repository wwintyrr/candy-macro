from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QSizePolicy, 
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,
)

import ui.css_styles as css_styles

# thanks gpt for this
on_off = [
    'Off <span style="color:red;">○</span>',
    'On <span style="color:lime;">●</span>'
]

# main class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # size and window config
        self.setWindowTitle("Candy Macro")
        self.setFixedSize(300, 100)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        # center
        central = QWidget()
        self.setCentralWidget(central)

        # layout
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # start/stop and on/off button
        button_layout = QHBoxLayout()

        self.main_button = QPushButton(f"Press to start macro")
        self.main_button.setStyleSheet(css_styles.button_style)
        self.main_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_label = QLabel("Macro: " + on_off[0])
        self.main_label.setStyleSheet(css_styles.label_style)

        button_layout.addWidget(self.main_label, 5)
        button_layout.addWidget(self.main_button, 5)

        self.main_status = QLabel("Current Status: " + "Stopped...")
        self.main_status.setStyleSheet(css_styles.borderless_label_style)

        # finalize
        layout.addWidget(self.main_status, 2)
        layout.addLayout(button_layout, 6)
        

    def setLabel(self, val=bool):
        if val == True:
            self.main_label.setText("Macro: " + on_off[1])
        else:
            self.main_label.setText("Macro: " + on_off[0])

    def setStatus(self, status=str):
        self.main_status.setText("Current Status: " + status + "...")
    
    # other
    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()