import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QPushButton,
    QWidget, QTextEdit, QSplitter, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt


class AddProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Project")
        self.layout = QFormLayout(self)

        # Add input fields
        self.id_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.owner_input = QLineEdit(self)

        self.layout.addRow("Project ID:", self.id_input)
        self.layout.addRow("Project Name:", self.name_input)
        self.layout.addRow("Project Owner:", self.owner_input)

        # Add buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

    def get_data(self):
        return {
            "id": self.id_input.text(),
            "name": self.name_input.text(),
            "owner": self.owner_input.text()
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Management")
        self.resize(800, 600)

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Left Panel: Table and Import Button
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)

        self.import_button = QPushButton("Import Project")
        self.import_button.clicked.connect(self.add_project)
        self.left_layout.addWidget(self.import_button)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Project ID", "Project Name", "Owner", "Status"])

        # Configure table to select rows and make it read-only (except status column)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemDoubleClicked.connect(self.show_details)
        self.left_layout.addWidget(self.table)

        self.layout.addWidget(self.left_panel)

        # Right Panel: Detail Viewer
        self.detail_view = QTextEdit()
        self.detail_view.setReadOnly(True)
        self.layout.addWidget(self.detail_view)

        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.detail_view)
        self.layout.addWidget(self.splitter)

    def add_project(self):
        dialog = AddProjectDialog()
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Insert read-only items into the table
            id_item = QTableWidgetItem(data["id"])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)

            name_item = QTableWidgetItem(data["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)

            owner_item = QTableWidgetItem(data["owner"])
            owner_item.setFlags(owner_item.flags() & ~Qt.ItemIsEditable)

            # Insert items into the table
            self.table.setItem(row_position, 0, id_item)
            self.table.setItem(row_position, 1, name_item)
            self.table.setItem(row_position, 2, owner_item)

            # Add a ComboBox for the status column
            status_combo = QComboBox()
            status_combo.addItems(["Pending", "In Progress", "Completed"])
            status_combo.setCurrentIndex(0)  # Default to "Pending"
            status_combo.currentIndexChanged.connect(
                lambda index, row=row_position: self.status_changed(row, index)
            )
            self.table.setCellWidget(row_position, 3, status_combo)

    def status_changed(self, row, index):
        combo = self.table.cellWidget(row, 3)  # Get the QComboBox
        new_status = combo.currentText()
        print(f"Status of project in row {row} changed to: {new_status}")

    def show_details(self, item):
        row = item.row()
        project_id = self.table.item(row, 0).text()
        project_name = self.table.item(row, 1).text()
        project_owner = self.table.item(row, 2).text()
        status_combo = self.table.cellWidget(row, 3)
        project_status = status_combo.currentText()

        details = (
            f"Project ID: {project_id}\n"
            f"Project Name: {project_name}\n"
            f"Project Owner: {project_owner}\n"
            f"Project Status: {project_status}"
        )
        self.detail_view.setText(details)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
