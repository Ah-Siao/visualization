import sys
import time  # Simulating heavy computations
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtk import vtkMolecule, vtkActor,vtkRenderer,vtkMoleculeMapper,vtkPeriodicTable

class MoleculeWorker(QThread):
    progress_updated = pyqtSignal(int)
    molecule_ready = pyqtSignal(vtkMolecule)

    def __init__(self, molecule_data):
        super().__init__()
        self.molecule_data = molecule_data

    def run(self):
        molecule = vtkMolecule()
        table = vtkPeriodicTable()

        # Simulate processing large molecules
        for i, atom in enumerate(self.molecule_data['atoms']):
            time.sleep(0.1)  # Simulate delay
            molecule.AppendAtom(table.GetAtomicNumber(atom[0]), *atom[1:])
            self.progress_updated.emit(int((i + 1) / len(self.molecule_data['atoms']) * 100))

        # Add bonds (optional for larger molecules, can also be part of atom processing)
        for bond in self.molecule_data['bonds']:
            molecule.AppendBond(bond[0], bond[1], bond[2])

        self.molecule_ready.emit(molecule)


class MoleculeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Interactive Molecule Viewer with Progress")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Add label
        layout.addWidget(QLabel("Rendering large molecules, please wait...", self))

        # Progress bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # VTK widget
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtk_widget)

        # VTK setup
        self.renderer = vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        # Simulate large molecule rendering
        self.init_large_molecule()

    def init_large_molecule(self):
        """Simulate initializing a large molecule."""
        # Example molecule data (use a larger dataset for real cases)
        molecule_data = {
            "atoms": [("C", 0.0, 0.0, 0.0), ("C", 1.5, 0.0, 0.0), ("H", -1.0, 0.0, 0.0), ("H", 2.5, 0.0, 0.0)],
            "bonds": [(0, 1, 1), (0, 2, 1), (1, 3, 1)]
        }

        self.worker = MoleculeWorker(molecule_data)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.molecule_ready.connect(self.display_molecule)

        self.worker.start()

    def display_molecule(self, molecule):
        """Render the molecule when it's ready."""
        # Reset progress bar
        self.progress_bar.setValue(0)

        colors = vtkNamedColors()

        # Create a molecule mapper and actor
        mapper = vtkMoleculeMapper()
        mapper.SetInputData(molecule)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d("SkyBlue"))

        # Add actor to the renderer
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(colors.GetColor3d("White"))

        # Start VTK rendering
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()
        self.interactor.Initialize()


def main():
    app = QApplication(sys.argv)
    widget = MoleculeWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
