from PyQt5.QtWidgets import (
    QApplication, QDialog, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
)
import sys


class ProjectTreeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Tree and Description Layout
        self.tree_desc_layout = QHBoxLayout()
        self.main_layout.addLayout(self.tree_desc_layout)

        # Tree Widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Projects")
        self.tree_widget.itemClicked.connect(self.display_project_description)
        self.tree_desc_layout.addWidget(self.tree_widget)

        # Description Box
        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        self.tree_desc_layout.addWidget(self.description_box)

        # Button Layout
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Centered Import Button
        self.import_button = QPushButton("Import Selected Project")
        self.import_button.clicked.connect(self.import_project)
        self.import_button.setFixedWidth(300)
        self.button_layout.addStretch()  # Add stretchable space on the left
        self.button_layout.addWidget(self.import_button)
        self.button_layout.addStretch()  # Add stretchable space on the right

        # Populate the tree
        self.populate_tree()

        # Currently selected project
        self.selected_project = None

    def populate_tree(self):
        # Example project data
        projects = {
            "Project A": "Description of Project A",
            "Project B": {
                "Subproject B1": "Description of Subproject B1",
                "Subproject B2": "Description of Subproject B2",
            },
            "Project C": "Description of Project C",
        }

        for project, description in projects.items():
            self.add_project(self.tree_widget, project, description)

    def add_project(self, parent, project_name, description):
        if isinstance(description, dict):
            # Parent node
            parent_item = QTreeWidgetItem(parent)
            parent_item.setText(0, project_name)
            for subproject, sub_desc in description.items():
                self.add_project(parent_item, subproject, sub_desc)
        else:
            # Leaf node
            item = QTreeWidgetItem(parent)
            item.setText(0, project_name)
            item.setData(0, 1, description)  # Store the description as item data

    def display_project_description(self, item, column):
        # Get the description from the item's data
        description = item.data(0, 1)
        if description:
            self.description_box.setText(description)
            self.selected_project = item.text(0)  # Save the selected project name
        else:
            self.description_box.clear()
            self.selected_project = None

    def import_project(self):
        if self.selected_project:
            # Show a confirmation message
            QMessageBox.information(self, "Project Imported", f"Selected Project: {self.selected_project}")
        else:
            # Show an error if no project is selected
            QMessageBox.warning(self, "No Selection", "Please select a project first.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectTreeDialog()
    dialog.exec_()
