from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDockWidget,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QToolButton
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
import sys


class CollapsibleSection(QWidget):
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.init_ui(title, content_widget)

    def init_ui(self, title, content_widget):
        self.layout = QVBoxLayout(self)
        #self.toggle_button = QPushButton(title)
        self.toggle_button=QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.RightArrow)
        #self.toggle_button.setCheckable(True)
        #self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.toggle)

        # Collapsible content
        self.content_area = QFrame()
        self.content_area.setLayout(QVBoxLayout())
        self.content_area.layout().addWidget(content_widget)
        self.content_area.setMinimumHeight(0)
        self.content_area.setMaximumHeight(0)  # Initially collapsed
        self.content_area.setSizePolicy(self.content_area.sizePolicy().Preferred, self.content_area.sizePolicy().Fixed)

        # Animation for collapsing/expanding
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.setDuration(300)  # Animation duration in ms

        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.content_area)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def toggle(self):
        # Adjust the height of the collapsible section
        if self.toggle_button.isChecked():
            self.content_area.setMaximumHeight(16777215)  # Expand
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.content_area.sizeHint().height())
        else:
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(0)  # Collapse
        self.animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Foldable Sections in QScrollArea")
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
        scroll_area.setWidgetResizable(True)

        # Create content widget for QScrollArea
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Add foldable sections
        for i in range(5):
            section_content = QLabel(f"Content for Section {i + 1}")
            section = CollapsibleSection(f"Section {i + 1}", section_content)
            content_layout.addWidget(section)

        content_layout.addStretch()
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
