from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton, QLabel, QDialog, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import time
import sys

# ThreadTask2 for handling different functions
class ThreadTask2(QThread):
    qthread_signal = pyqtSignal(str)

    def __init__(self, input_function, parent=None):
        super().__init__(parent)
        self.input_function = input_function

    def run(self):
        self.qthread_signal.emit(f"Start searching {self.input_function.__name__}")
        self.input_function()
        self.qthread_signal.emit("Finish")


def input_function1():
    time.sleep(1)
    print('finish searching fxn1')
    return 0


def input_function2():
    time.sleep(2)
    print('finish searching fxn2')
    return 1


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progress")
        self.setGeometry(200, 200, 300, 100)

        # Create progress bar and label
        self.layout = QVBoxLayout(self)
        self.progress_label = QLabel("Initializing...")
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  

        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)

    def update_progress(self, message):
        self.progress_label.setText(message)

    def complete(self):
        self.accept()  # Close the dialog


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TEST")
        self.setGeometry(100, 100, 1200, 600)

        # Create push button
        self.pushbutton = QPushButton("Start Progress", self)
        self.pushbutton.setGeometry(100, 150, 200, 50)
        self.pushbutton.clicked.connect(self.button_click)

    def button_click(self):
        # Create progress dialog
        self.progress_dialog = ProgressDialog(self)

        # Create threads
        self.qthread1 = ThreadTask2(input_function1)
        self.qthread2 = ThreadTask2(input_function2)

        # Connect signals
        self.qthread1.qthread_signal.connect(self.update_progress)
        self.qthread1.finished.connect(self.qthread2.start)  # Start qthread2 after qthread1 finishes
        self.qthread1.finished.connect(self.check_completion)

        self.qthread2.qthread_signal.connect(self.update_progress)
        self.qthread2.finished.connect(self.check_completion)

        # Show progress dialog and start the first thread
        self.progress_dialog.show()
        self.qthread1.start()

    def update_progress(self, message):
        self.progress_dialog.update_progress(message)

    def check_completion(self):
        if not self.qthread1.isRunning() and not self.qthread2.isRunning():
            self.progress_dialog.complete()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindowController()
    widget.show()
    sys.exit(app.exec_())
