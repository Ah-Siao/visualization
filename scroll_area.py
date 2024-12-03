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
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QScrollArea in QDockWidget Example")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QLabel("Main Window Content")
        central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)

        # Create QDockWidget
        dock = QDockWidget("Dockable Widget", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Enable resizing of content with scroll area
        scroll_area.setSizePolicy(scroll_area.sizePolicy().Expanding, scroll_area.sizePolicy().Expanding)

        # Create content widget for QScrollArea
        content_widget = QWidget()
        content_layout = QVBoxLayout()

        # Add some sample widgets to the content widget
        for i in range(20):
            label = QLabel(f"Label {i + 1}")
            button = QPushButton(f"Button {i + 1}")
            content_layout.addWidget(label)
            content_layout.addWidget(button)

        content_widget.setLayout(content_layout)

        # Set the content widget as the widget for the QScrollArea
        scroll_area.setWidget(content_widget)

        # Add the scroll area to the dock widget
        dock.setWidget(scroll_area)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        # Add the dock widget to the main window
        self.addDockWidget(Qt.RightDockWidgetArea, dock)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
