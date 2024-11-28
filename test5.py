import sys
import vtk
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MoleculeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Molecule Editor")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # VTK widget and toggle button
        self.vtk_widget = QVTKRenderWindowInteractor(self.main_widget)
        self.toggle_button = QPushButton("Toggle Selection Mode", self.main_widget)
        self.toggle_button.clicked.connect(self.toggle_selection_mode)

        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.vtk_widget)
        layout.addWidget(self.toggle_button)

        # Initialize variables
        self.selection_mode = False
        self.selected_atoms = []
        self.start_pos = None
        self.dragging = False

        # Initialize VTK components
        self.init_vtk()

    def init_vtk(self):
        # Create molecule
        self.molecule = vtk.vtkMolecule()
        oxygen = self.molecule.AppendAtom(8, 0.0, 0.0, 0.0)  # Oxygen
        hydrogen1 = self.molecule.AppendAtom(1, 0.96, 0.0, 0.0)  # Hydrogen 1
        hydrogen2 = self.molecule.AppendAtom(1, -0.48, 0.88, 0.0)  # Hydrogen 2
        self.molecule.AppendBond(oxygen, hydrogen1, 1)
        self.molecule.AppendBond(oxygen, hydrogen2, 1)

        # Mapper and actor for molecule
        self.molecule_mapper = vtk.vtkMoleculeMapper()
        self.molecule_mapper.SetInputData(self.molecule)
        self.molecule_mapper.UseBallAndStickSettings()
        self.molecule_actor = vtk.vtkActor()
        self.molecule_actor.SetMapper(self.molecule_mapper)

        # Renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.molecule_actor)
        self.renderer.SetBackground(1, 1, 1)  # White background

        # Add to VTK widget
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()

        # Picker for selecting atoms
        self.picker = vtk.vtkCellPicker()
        self.picker.SetTolerance(0.01)

        # Add event observers
        self.interactor.AddObserver("LeftButtonPressEvent", self.on_left_button_down)
        self.interactor.AddObserver("LeftButtonReleaseEvent", self.on_left_button_up)
        self.interactor.AddObserver("MouseMoveEvent", self.on_mouse_move)

    def toggle_selection_mode(self):
        """Toggle between selection and dragging modes."""
        self.selection_mode = not self.selection_mode
        if self.selection_mode:
            self.toggle_button.setText("Exit Selection Mode")
            print("Selection mode enabled.")
        else:
            self.toggle_button.setText("Toggle Selection Mode")
            print("Selection mode disabled. Selected atoms cleared.")
            self.selected_atoms = []

    def on_left_button_down(self, obj, event):
        """Handle mouse press events."""
        if self.selection_mode:
            # Start selection
            self.start_pos = self.interactor.GetEventPosition()
            print(f"Selection started at {self.start_pos}")
        elif self.selected_atoms:
            # Start dragging
            self.dragging = True

    def on_left_button_up(self, obj, event):
        """Handle mouse release events."""
        if self.selection_mode:
            # Complete selection
            click_pos = self.interactor.GetEventPosition()
            self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)
            picked_pos = self.picker.GetPickPosition()

            # Check for picked atoms
            self.selected_atoms = self.get_picked_atoms(picked_pos)
            print(f"Selected atoms: {self.selected_atoms}")
        elif self.dragging:
            # Stop dragging
            self.dragging = False

    def on_mouse_move(self, obj, event):
        """Handle mouse move events."""
        if self.dragging and self.selected_atoms:
            mouse_pos = self.interactor.GetEventPosition()
            self.renderer.SetDisplayPoint(mouse_pos[0], mouse_pos[1], 0.0)
            self.renderer.DisplayToWorld()
            world_coords = self.renderer.GetWorldPoint()[:3]

            for atom_id in self.selected_atoms:
                self.molecule.SetAtomPosition(atom_id, world_coords)
            self.vtk_widget.GetRenderWindow().Render()

    def get_picked_atoms(self, picked_pos):
        """Return the atoms nearest to the picked position."""
        picked_atoms = []
        for atom_id in range(self.molecule.GetNumberOfAtoms()):
            atom_pos = self.molecule.GetAtomPosition(atom_id)
            distance = ((picked_pos[0] - atom_pos[0]) ** 2 +
                        (picked_pos[1] - atom_pos[1]) ** 2 +
                        (picked_pos[2] - atom_pos[2]) ** 2) ** 0.5
            if distance < 0.5:  # Threshold for selection
                picked_atoms.append(atom_id)
        return picked_atoms


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoleculeEditor()
    window.show()
    sys.exit(app.exec_())
