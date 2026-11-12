from ui.main_window import MainWindow
from core.macro import MacroWorker

from PySide6.QtWidgets import QApplication

"""
state mapping:

idle ->

first ->

second ->

buy ->
(after 2 cycles buy rare chest)
"""

def main():

    app = QApplication([])
    window = MainWindow()

    window.worker = None

    def worker_finished():
        window.main_button.setText("Press to start macro")
        window.setLabel(False)
    
    def toggle():
        if window.worker is not None and window.worker.isRunning():
            window.worker.stop()
            window.main_button.setText("Press to start macro")
            window.setLabel(False)
            return

        window.worker = MacroWorker()

        window.worker.finished.connect(worker_finished)
        window.worker.status_changed.connect(window.setStatus)

        window.worker.start()

        window.main_button.setText("Press to stop macro")
        window.setLabel(True)

    window.main_button.clicked.connect(toggle)

    window.show()
    app.exec()

# entry
if __name__ == "__main__":
    main()