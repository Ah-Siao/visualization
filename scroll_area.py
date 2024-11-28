import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDockWidget,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QDockWidget with Scrollable Content")
        self.setGeometry(100, 100, 800, 600)

        # Create a dock widget
        dock = QDockWidget("Scrollable Dock", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the content
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Add many widgets to make it scrollable
        for i in range(30):
            layout.addWidget(QLabel(f"Label {i+1}"))
            layout.addWidget(QPushButton(f"Button {i+1}"))

        # Set the content widget as the scroll area's widget
        scroll_area.setWidget(content_widget)

        # Set the scroll area as the dock widget's widget
        dock.setWidget(scroll_area)

        # Add the dock widget to the main window
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
