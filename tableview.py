import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class DemoTableView(QDialog):
    def __init__(self, result_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Table View")
        self.setGeometry(200, 200, 400, 300)

        self.table = QTableWidget()
        self.table.setRowCount(len(result_dict))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Key", "Value"])
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: lightblue; /* Background color */
                color: darkblue;            /* Text color */
                font-weight: bold;          /* Bold text */
                border: 1px solid black;    /* Optional border */
            }
        """)

        for row, (key, value) in enumerate(result_dict.items()):
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value))

            key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
            bold_font = QFont()
            bold_font.setBold(True)
            key_item.setFont(bold_font)

            value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
            value_item.setForeground(QColor("red"))

            self.table.setItem(row, 0, key_item)
            self.table.setItem(row, 1, value_item)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)

        # Sample dictionary result
        self.result_dict = {
            "Name": "John Doe",
            "Age": 30,
            "Location": "New York",
        }

        # Create a button
        self.button = QPushButton("Show Result")
        self.button.clicked.connect(self.show_result_viewer)

        # Set layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        container.setLayout(layout)

        self.setCentralWidget(container)

    def show_result_viewer(self):
        self.result_viewer = DemoTableView(self.result_dict, self)
        self.result_viewer.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
