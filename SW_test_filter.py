from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QTableWidget, QTextEdit, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt


class FilterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)

    def set_filters(self, filter_config):
        # Clear existing filters
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Add new filters
        for config in filter_config:
            if config["type"] == "checkbox":
                checkbox = QCheckBox(config["label"], self)
                self.main_layout.addWidget(checkbox)
            elif config["type"] == "lineedit":
                label = QLabel(config["label"], self)
                lineedit = QLineEdit(self)
                self.main_layout.addWidget(label)
                self.main_layout.addWidget(lineedit)
            elif config["type"] == "combobox":
                label = QLabel(config["label"], self)
                combobox = QComboBox(self)
                combobox.addItems(config.get("options", []))
                self.main_layout.addWidget(label)
                self.main_layout.addWidget(combobox)

        # Add spacer to push filters to the top
        self.main_layout.addStretch()




filter_dict ={"Project A": [
                {"type": "checkbox", "label": "Include Subcategories"},
                {"type": "lineedit", "label": "Search Term"},
                {"type": "combobox", "label": "Type", "options": ["Option 1", "Option 2", "Option 3"]}
            ],
            "Project B": [
                {"type": "lineedit", "label": "Compound Name"},
                {"type": "combobox", "label": "State", "options": ["Solid", "Liquid", "Gas"]}
            ],
            "Project C": [
                {"type": "checkbox", "label": "Enable Advanced Search"},
                {"type": "lineedit", "label": "Filter by Author"}
            ]}


class DatabaseSearchWidget(QWidget):
    def __init__(self, db_path,filter_dict):
        super().__init__()
        self.db_path = db_path
        self.filter_configs =  filter_dict
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Search with Dynamic Filters")
        self.setGeometry(100, 100, 1200, 600)
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()

        # Project Selector
        self.project_selector = QComboBox(self)
        self.project_selector.addItems(self.filter_configs.keys())  
        self.project_selector.currentIndexChanged.connect(self.update_filters)
        left_layout.addWidget(self.project_selector)

        # Filter Panel
        self.filter_panel = FilterPanel(self)
        left_layout.addWidget(self.filter_panel)

        # Search Input
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search term")
        left_layout.addWidget(self.search_input)

        # Search Button
        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.perform_search)
        left_layout.addWidget(search_button)

        # Search Results
        self.results_table = QTableWidget(self)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.itemSelectionChanged.connect(self.show_details)
        left_layout.addWidget(self.results_table)

        main_layout.addLayout(left_layout)

        # Middle column: Details
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(QLabel("Details", self))

        self.detail_view = QTextEdit(self)
        self.detail_view.setReadOnly(True)
        middle_layout.addWidget(self.detail_view)

        main_layout.addLayout(middle_layout)

        # Right column: Visualization
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Visualization", self))

        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # Load initial filters for the first project
        self.update_filters(0)


    def update_filters(self, index):
        project_name = self.project_selector.currentText()
        filter_config = self.filter_configs.get(project_name, [])
        self.filter_panel.set_filters(filter_config)

    def perform_search(self):
        print("Performing search...")

    def show_details(self):
        print("Showing details of selected item...")


if __name__ == "__main__":
    app = QApplication([])

    # Initialize the widget
    window = DatabaseSearchWidget("path_to_database",filter_dict)
    window.show()

    app.exec_()
