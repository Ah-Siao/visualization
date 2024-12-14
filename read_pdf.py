from PyQt5.QtWidgets import (
    QApplication, QDialog, QTreeWidget, QTreeWidgetItem,
    QScrollArea, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLabel, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
import fitz  # PyMuPDF
from PyQt5 import Qt

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
        self.tree_widget.itemClicked.connect(self.display_project_content)
        self.tree_desc_layout.addWidget(self.tree_widget)

        # Scroll Area for Content (PDF or Images)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)  # Use QVBoxLayout for flexibility
        self.content_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.content_layout.setSpacing(0)  # Remove spacing
        self.scroll_area.setWidget(self.content_container)
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
        # Example project data (each project could have images or PDFs)
        projects = {
            "Project A": "m3gnet.pdf",  
            "Project B": "m3gnet.pdf",  
            "Project C": "m3gnet.pdf", 
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
            # Leaf node (either images or PDF)
            item = QTreeWidgetItem(parent)
            item.setText(0, project_name)
            item.setData(0, 1, description)  # Store the content (images or PDF)

    def display_project_content(self, item, column):
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Get the content associated with the selected project
        content = item.data(0, 1)
        if isinstance(content, str) and content.endswith(".pdf"):
            # Handle PDF (if the content is a PDF path)
            self.display_pdf(content)
        else:
            self.selected_project = None

    def display_pdf(self, pdf_path):
        self.selected_project = "PDF"
        # Render the first page of the PDF using PyMuPDF
        doc = fitz.open(pdf_path)
        for page_nb in range(doc.page_count):
            page = doc.load_page(page_nb)  # Load the first page
            pix = page.get_pixmap()
            img_data = pix.tobytes("ppm")

            # Convert to QImage and then QPixmap
            q_image = QImage(img_data, pix.width, pix.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            # Display PDF page in a QLabel
            label = QLabel()
            label.setPixmap(pixmap)
            self.content_layout.addWidget(label)

    def import_project(self):
        if self.selected_project:
            QMessageBox.information(self, "Project Imported", f"Selected Project: {self.selected_project}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a project first.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectTreeDialog()
    dialog.exec_()
