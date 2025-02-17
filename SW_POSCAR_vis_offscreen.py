import vtk
import ase.io as ase_io
import numpy as np
import json
from pymatgen.analysis.local_env import EconNN, CrystalNN
import sys
from pymatgen.core import Structure



with open("atomic_data.json",'r') as f:
    data=json.load(f)
atom_colors={value['atomic_number']: value['color'] for value in data.values()}


def create_atom_color_table(atom_colors):
    lut = vtk.vtkLookupTable()
    # Allow mapping of atomic numbers up to 255
    lut.SetNumberOfTableValues(256)  
    lut.Build()
    # Set default for unrecognized atoms
    lut.SetTableValue(0, 0, 0, 0, 1.0)  
    for atomic_number, color in atom_colors.items():
        r, g, b = color
        lut.SetTableValue(atomic_number, r, g, b, 1.0) 
    return lut


def find_site_index(site, structure):
    # Iterate over all sites in the structure and compare their fractional coordinates
    for i, s in enumerate(structure):
        if np.allclose(site.frac_coords, s.frac_coords, atol=1e-5):
            return i
    return -1  



def save_render_as_image(render_window, filename='output_image.png'):
    scale=2
    width,height=render_window.GetSize()
    render_window.SetSize(width*scale,height*scale)
    # Create an image filter
    window_to_image_filter = vtk.vtkWindowToImageFilter()
    window_to_image_filter.SetInput(render_window)
    window_to_image_filter.SetScale(scale) # Increase resolution
    #window_to_image_filter.SetInputBufferTypeToRGBA() #Preserve colors
    window_to_image_filter.ReadFrontBufferOff()  # Read from the back buffer
    window_to_image_filter.Update()

    # Create an image writer
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInputConnection(window_to_image_filter.GetOutputPort())
    writer.Write()




def view_POSCAR(file,bond_method=EconNN()):
    # prepared Material for visualization
    bond_nn=bond_method
    atoms=ase_io.read(file)
    structure=Structure(
        lattice=atoms.cell,
        species=atoms.get_chemical_symbols(),
        coords=atoms.get_scaled_positions()
    )
    lattice=[vtk.vtkVector3d(atoms.cell[i]) for i in range(len(atoms.cell))]
    unique_atoms={syb:data[syb]['atomic_number'] for syb in set(atoms.get_chemical_symbols())}
    bond_index=[]
    for i, site in enumerate(structure):
        nn_info=bond_nn.get_nn_info(structure,i)
        for item in nn_info:
            site, _, weight,_=item.values()
            neighbor_index=find_site_index(site,structure)
            if neighbor_index!=-1 and weight>0.1:
                bond_index.append([i,neighbor_index])    
    num_species=len(structure.species)
    mol=vtk.vtkMolecule()
    mol.SetLattice(*lattice)
    for i in range(num_species):
        x,y,z=structure.cart_coords[i]
        atom_nb=structure.atomic_numbers[i]
        mol.AppendAtom(atom_nb,x,y,z)
    for bond in bond_index:
        mol.AppendBond(bond[0],bond[1],1)
    molecule_mapper = vtk.vtkMoleculeMapper()
    molecule_mapper.SetInputData(mol)
    molecule_mapper.UseBallAndStickSettings()
    lut = create_atom_color_table(atom_colors)

    ### Add legend
    legend=vtk.vtkLegendBoxActor()
    legend.SetNumberOfEntries(len(unique_atoms))
    for i, (atom_syb,atom_nb) in enumerate(unique_atoms.items()):
        color=lut.GetTableValue(atom_nb)[:3]
        sphere=vtk.vtkSphereSource()
        sphere.SetRadius(0.2)
        sphere.Update()
        mapper=vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor=vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        legend.SetEntry(i, actor.GetMapper().GetInput(), atom_syb, color)

    legend.SetPosition(0.75, 0.05) 
    legend.SetWidth(0.2)
    legend.SetHeight(0.15)
    legend.UseBackgroundOn()
    legend.SetBackgroundColor(0,0,0)  

    molecule_actor = vtk.vtkActor()
    molecule_actor.SetMapper(molecule_mapper)  

    renderer = vtk.vtkRenderer()
    renderer.AddActor(molecule_actor)
    renderer.SetBackground(0.1, 0.1, 0.2) 
    renderer.AddActor(legend)

    render_window = vtk.vtkRenderWindow()
    render_window.SetOffScreenRendering(True)
    render_window.AddRenderer(renderer)
    render_window.SetWindowName("Visualization")
    #render_window_interactor = vtk.vtkRenderWindowInteractor()
    #render_window_interactor.SetRenderWindow(render_window)

    camera=renderer.GetActiveCamera()
    camera.SetPosition(3,3,3)
    camera.SetFocalPoint(0.1, 0.1, 0.0)
    camera.SetViewUp(0, 0, 1) 
    renderer.ResetCamera()
    render_window.SetSize(800, 800)
    render_window.Render()
    save_render_as_image(render_window, 'test.png')
    #render_window_interactor.Start()




if __name__=="__main__":
    view_POSCAR("mp_1199165_POSCAR")

