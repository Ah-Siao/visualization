import vtk

# Create a vtkMolecule object
molecule = vtk.vtkMolecule()

# Add atoms: O (Oxygen), H (Hydrogen)
oxygen = molecule.AppendAtom(8, 0.0, 0.0, 0.0)  # Oxygen at the origin
hydrogen1 = molecule.AppendAtom(1, 0.96, 0.0, 0.0)  # Hydrogen 1
hydrogen2 = molecule.AppendAtom(1, -0.48, 0.88, 0.0)  # Hydrogen 2

# Add bonds
molecule.AppendBond(oxygen, hydrogen1, 1)  # Single bond between O and H1
molecule.AppendBond(oxygen, hydrogen2, 1)  # Single bond between O and H2

# Set up a molecule mapper to visualize the molecule
molecule_mapper = vtk.vtkMoleculeMapper()
molecule_mapper.SetInputData(molecule)
molecule_mapper.UseBallAndStickSettings()

# Set up the actor
molecule_actor = vtk.vtkActor()
molecule_actor.SetMapper(molecule_mapper)

# Set up the renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(molecule_actor)
renderer.SetBackground(255, 255, 255)  # Dark background

# Set up the render window and interactor
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Move Atoms in Molecule")

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# State to track interaction
selected_atom_id = None
dragging = False

# Helper function to find the nearest atom to the mouse click
def find_nearest_atom(click_pos):
    min_distance = float("inf")
    nearest_atom_id = None

    for atom_id in range(molecule.GetNumberOfAtoms()):
        # Get atom position in world coordinates
        atom_pos = molecule.GetAtomPosition(atom_id)

        # Convert world coordinates to display (screen) coordinates
        renderer.SetWorldPoint(atom_pos[0], atom_pos[1], atom_pos[2], 1.0)
        renderer.WorldToDisplay()
        display_coords = renderer.GetDisplayPoint()

        # Compute distance from the click position to the atom's screen position
        distance = ((display_coords[0] - click_pos[0]) ** 2 +
                    (display_coords[1] - click_pos[1]) ** 2) ** 0.5

        if distance < min_distance:
            min_distance = distance
            nearest_atom_id = atom_id

    return nearest_atom_id

# Callback to handle right mouse button press
def on_right_button_down(obj, event):
    global selected_atom_id, dragging
    click_pos = render_window_interactor.GetEventPosition()
    selected_atom_id = find_nearest_atom(click_pos)

    if selected_atom_id is not None:
        dragging = True
        position = molecule.GetAtomPosition(selected_atom_id)
        print(f"Atom {selected_atom_id} selected at position {position}")

# Callback to handle mouse movement while right button is pressed
def on_mouse_move(obj, event):
    global selected_atom_id, dragging
    if dragging and selected_atom_id is not None:
        # Get the new mouse position and convert it to world coordinates
        mouse_pos = render_window_interactor.GetEventPosition()
        renderer.SetDisplayPoint(mouse_pos[0], mouse_pos[1], 0.0)
        renderer.DisplayToWorld()
        world_coords = renderer.GetWorldPoint()[:3]

        # Move the selected atom to the new position
        molecule.SetAtomPosition(selected_atom_id, world_coords)
        print(f"Atom {selected_atom_id} dragged to position {world_coords}")
        render_window.Render()

# Callback to handle right mouse button release
def on_right_button_up(obj, event):
    global selected_atom_id, dragging
    if dragging and selected_atom_id is not None:
        # Stop dragging and finalize the atom's position
        final_position = molecule.GetAtomPosition(selected_atom_id)
        print(f"Atom {selected_atom_id} released at position {final_position}")
        selected_atom_id = None
        dragging = False
        render_window.Render()

# Add observers for right mouse button events
render_window_interactor.RemoveObservers('RightButtonPressEvent')
render_window_interactor.AddObserver("RightButtonPressEvent", on_right_button_down,1.0)
render_window_interactor.AddObserver("MouseMoveEvent", on_mouse_move)
render_window_interactor.AddObserver("RightButtonReleaseEvent", on_right_button_up,-1.0)

# Start the visualization
render_window.Render()
render_window_interactor.Start()
