import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QTextEdit
)
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
from vtk import vtkMoleculeMapper, vtkPeriodicTable, vtkSimpleBondPerceiver,vtkActor
from vtkmodules.vtkCommonDataModel import vtkMolecule
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class DatabaseSearchWidget(QWidget):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Database Search with VTK Molecule Visualization")
        self.setGeometry(100, 100, 1200, 600)

        # Main layout
        main_layout = QHBoxLayout(self)

        # Left column: Search results
        left_layout = QVBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search term")
        left_layout.addWidget(self.search_input)

        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.perform_search)
        left_layout.addWidget(search_button)

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

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        right_layout.addWidget(self.vtk_widget)

        main_layout.addLayout(right_layout)

        # VTK setup
        self.renderer = vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

    def perform_search(self):
        search_term = self.search_input.text()
        if not search_term.strip():
            self.results_table.setRowCount(0)
            self.detail_view.clear()
            self.clear_visualization()
            return

        # Connect to the database and perform the search
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = "SELECT id, name, structure FROM your_table WHERE name LIKE ?"
            cursor.execute(query, (f"%{search_term}%",))
            results = cursor.fetchall()

            # Set table headers
            column_names = ["ID", "Name"]
            self.results_table.setRowCount(len(results))
            self.results_table.setColumnCount(len(column_names))
            self.results_table.setHorizontalHeaderLabels(column_names)

            # Populate the table
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data[:2]):
                    self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            # Store full results for use in detail and visualization views
            self.full_results = {row[0]: row for row in results}

            conn.close()

        except sqlite3.Error as e:
            self.results_table.setRowCount(0)
            self.detail_view.clear()
            self.clear_visualization()

    def show_details(self):
        selected_items = self.results_table.selectedItems()
        if not selected_items:
            return

        # Get selected row's ID
        selected_id = int(self.results_table.item(self.results_table.currentRow(), 0).text())
        selected_row = self.full_results.get(selected_id)

        # Update details view
        self.detail_view.setPlainText(f"ID: {selected_row[0]}\nName: {selected_row[1]}\nStructure: {selected_row[2]}")

        # Update VTK visualization
        structure_data = selected_row[2]
        self.visualize_structure(structure_data)

    def visualize_structure(self, structure_data):
        """Visualizes a molecular structure using vtkMolecule."""
        molecule = self.create_vtk_molecule(structure_data)

        # Create mapper and actor for vtkMolecule
        mapper = vtkMoleculeMapper()
        mapper.SetInputData(molecule)

        actor = vtkActor()
        actor.SetMapper(mapper)

        # Update the renderer
        self.renderer.RemoveAllViewProps()
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def create_vtk_molecule(self, structure_data):
        """Creates a vtkMolecule object from structure data."""
        molecule = vtkMolecule()
        table = vtkPeriodicTable()
        bond_perceiver = vtkSimpleBondPerceiver()
        colors = vtkNamedColors()

        # Example: add atoms manually (you'll need to parse structure_data to add atoms properly)
        molecule.AppendAtom(table.GetAtomicNumber("C"), 0.0, 0.0, 0.0)
        molecule.AppendAtom(table.GetAtomicNumber("C"), 1.4, 0.0, 0.0)

        # Add a bond between the two atoms
        bond_perceiver.SetInputData(molecule)
        bond_perceiver.Update()

        return molecule

    def clear_visualization(self):
        """Clears the VTK visualization."""
        self.renderer.RemoveAllViewProps()
        self.vtk_widget.GetRenderWindow().Render()


def main():
    app = QApplication(sys.argv)

    # Provide the path to your SQLite database
    db_path = "your_database.db"

    # Create a sample database for demonstration (optional)
    create_sample_database(db_path)

    window = DatabaseSearchWidget(db_path)
    window.show()
    window.interactor.Initialize()  # Initialize the VTK interactor

    sys.exit(app.exec_())


def create_sample_database(db_path):
    """Creates a sample SQLite database for demonstration purposes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a sample table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS your_table (
        id INTEGER PRIMARY KEY,
        name TEXT,
        structure TEXT
    )
    """)

    # Insert sample data
    cursor.executemany("""
    INSERT INTO your_table (name, structure) VALUES (?, ?)
    """, [
        ("Benzene", "C1=CC=CC=C1"),
        ("Methane", "CH4"),
    ])

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
