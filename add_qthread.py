from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton, QStatusBar, QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import time
import sys

# With for loop:
class ThreadTask(QThread):
    # Signal to update the progress bar
    qthread_signal = pyqtSignal(int)
    def run(self):
        """The run method is executed in the new thread."""
        max_value = 100
        for i in range(max_value):
            time.sleep(0.01)  # Simulate a time-consuming task
            self.qthread_signal.emit(i + 1)


def input_function1():
    time.sleep(1)
    print('finish searching fxn1')
    return 0

def input_function2():
    time.sleep(2)
    print('finish searching fxn2')
    return 1

class ThreadTask2(QThread):
    # Signal for string
    qthread_signal=pyqtSignal(str)
    def __init__(self,input_function,parent=None):
        super().__init__(parent)
        self.input_function=input_function
    def run(self):
        if self.input_function is input_function1:
            self.qthread_signal.emit('Start searching fxn1')
            self.input_function()
            self.qthread_signal.emit('Finish')
        elif self.input_function is input_function2:
            self.qthread_signal.emit('Start searching fxn2')
            self.input_function()
            self.qthread_signal.emit('Finish')
        else:
            pass

class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TEST")
        self.setGeometry(100, 100, 1200, 600)
        # Create progress bar at statusbar region
        self.progresscombo=QWidget()
        self.progresslayout=QHBoxLayout()

        self.progressbar = QProgressBar(self)
        self.progressbar.setMaximum(100)
        #self.progressbar.setFixedWidth(150)
        self.progressbar.hide()
        self.progresslabel=QLabel()
        self.progressbar.setFixedWidth(150)
        self.progresslabel.hide()
        self.progresslayout.addWidget(self.progresslabel,1)
        self.progresslayout.addWidget(self.progressbar,1)
        self.progresscombo.setLayout(self.progresslayout)
        self.progresscombo.setFixedWidth(300)
        # Create statusbar
        statusbar=QStatusBar(self)
        statusbar.addWidget(self.progresscombo,1)
        self.setStatusBar(statusbar)

        # Create push button
        self.pushbutton = QPushButton("Start Progress", self)
        self.pushbutton.setGeometry(100, 150, 200, 50)
        self.pushbutton.clicked.connect(self.button_click)
        self.stop_progress()

 
    def button_click(self):
        self.progressbar.show()
        # Create thread instance
        #self.qthread=ThreadTask()
        self.qthread = ThreadTask2(input_function1)
        self.qthread2=ThreadTask2(input_function2)
        # Connect signal from thread to the slot in main thread
        # self.qthread.qthread_signal.connect(self.progress_changed)
        self.qthread.qthread_signal.connect(self.progress_undetermine)
        self.qthread2.qthread_signal.connect(self.progress_undetermine)
        # Start the thread
        self.qthread2.start()
        self.qthread.start()

    def progress_changed(self, value):
        # Update progress bar
        self.progressbar.setValue(value)
    
    def stop_progress(self):
        self.progressbar.setRange(0,100)
        self.progressbar.setValue(100)
    
    def progress_undetermine(self,value):
        self.progressbar.setRange(0,0)
        self.progresslabel.show()
        self.progresslabel.setText(value)
        
        if value =='Finish':
            self.stop_progress()
            self.progresslabel.setText(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindowController()
    widget.show()
    sys.exit(app.exec_())
