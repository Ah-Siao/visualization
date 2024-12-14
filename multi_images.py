from PyQt5.QtWidgets import (
    QApplication, QDialog, QTreeWidget, QTreeWidgetItem,
    QScrollArea, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLabel, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np


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
        self.tree_widget.itemClicked.connect(self.display_project_images)
        self.tree_desc_layout.addWidget(self.tree_widget)

        # Scroll Area for Images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.image_layout = QGridLayout(self.image_container)  # Use QGridLayout to fill the space
        self.image_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.image_layout.setSpacing(0)  # Remove spacing
        self.scroll_area.setWidget(self.image_container)
        self.tree_desc_layout.addWidget(self.scroll_area)

        # Button Layout
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Centered Import Button
        self.import_button = QPushButton("Import Selected Project")
        self.import_button.clicked.connect(self.import_project)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.import_button)
        self.button_layout.addStretch()

        # Populate the tree
        self.populate_tree()

        # Currently selected project
        self.selected_project = None

    def populate_tree(self):
        # Example project data (Each project has an associated array of images)
        projects = {
            "Project A": self.generate_dummy_images(8),  # 8 dummy images
            "Project B": {
                "Subproject B1": self.generate_dummy_images(6),  # 6 dummy images
                "Subproject B2": self.generate_dummy_images(9),  # 9 dummy images
            },
            "Project C": self.generate_dummy_images(12),  # 12 dummy images
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
            item.setData(0, 1, description)  # Store the image array as item data

    def display_project_images(self, item, column):
        # Clear existing images
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Get the images associated with the selected project
        images = item.data(0, 1)
        if isinstance(images, list):
            self.selected_project = item.text(0)

            # Dynamically arrange images in grid
            row, col = 0, 0
            max_columns = 3  # Number of images per row
            for img in images:
                # Convert image array to QPixmap
                height, width, channel = img.shape
                bytes_per_line = channel * width
                q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)

                # Add image to layout
                label = QLabel()
                label.setPixmap(pixmap.scaled(200, 200))  # Scale for consistent size
                label.setFixedSize(200, 200)  # Set fixed size
                self.image_layout.addWidget(label, row, col)

                # Update row and column
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
        else:
            self.selected_project = None

    def import_project(self):
        if self.selected_project:
            # Show a confirmation message
            QMessageBox.information(self, "Project Imported", f"Selected Project: {self.selected_project}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a project first.")

    def generate_dummy_images(self, count):
        """
        Generate a list of dummy images as NumPy arrays.
        Replace this with your actual image array source.
        """
        images = []
        for _ in range(count):
            # Create a 100x100 RGB image with random colors
            img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            images.append(img)
        return images


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectTreeDialog()
    dialog.exec_()
