import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
)
import matplotlib.pyplot as plt
import numpy as np


class GraphWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Graph Viewer")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plot_sample_graph()
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_sample_graph(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        ax = self.figure.add_subplot(111)
        ax.clear() 
        ax.plot(x, y, label="y = sin(x)")
        ax.set_title("Sample Graph")
        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.legend()
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)
        self.button = QPushButton("Show Graph")
        self.button.clicked.connect(self.show_graph_widget)
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_graph_widget(self):
        self.graph_widget = GraphWidget(self)
        self.graph_widget.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
