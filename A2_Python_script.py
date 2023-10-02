import ifcopenshell
import ifcopenshell.util.element
from pathlib import Path

modelname = "LLYN - STRU"

# Code from teacher Martina for testing
try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Your script goes here
# 1. part: count elements 
beams = model.by_type('IfcBeam')
columns = model.by_type('IfcColumn')
slab = model.by_type('IfcSlab')

print('beams: ', len(beams))
print('columns: ', len(columns))
print('slab: ', len(slab))



#2. part: assign nodes to the elements
def assign_nodes_to_elements(model):
    elements = []

    for element in model.by_type('IfcColumn'):
        nodes = get_nodes_from_geometry(element)
        columns.append({'element_id': element.id(), 'nodes': nodes})

    for element in model.by_type('IfcBeam'):
        nodes = get_nodes_from_geometry(element)
        beams.append({'element_id': element.id(), 'nodes': nodes})

    # maybe slabs too???

    return elements

def get_nodes_from_geometry(element):
# Here we have to analyze the geometry information of the element and extract the corresponding nodes. 
# This could be complex and depends on the structure of our IFC file.
# Here is an example:

    nodes = []

    # if 'Representation' in element:
    #     representation = element.Representation
    #     for item in representation.Items:
    #         if 'Coordinates' in item:
    #             coordinates = item.Coordinates
    #             for coord in coordinates:
    #                 nodes.append({'x': coord[0], 'y': coord[1], 'z': coord[2]})

    element = model.by_type('IfcBeam')

    if hasattr(element, "ObjectPlacement"):

    # Zugriff auf die globalen Koordinaten (doesn't work)
        global_coordinates = element.ObjectPlacement.RelativePlacement.Location.Coordinates
        print("Globale Koordinaten des Elements:", global_coordinates)

    else:
        print("Das Element hat keine 'ObjectPlacement'-Informationen.")

    return nodes


#3. part: create structural model
if __name__ == '__main__':
    ifc_file = model

    elements = assign_nodes_to_elements(ifc_file)

elements = assign_nodes_to_elements(model)

for element in elements:
        print(f"Element ID: {element['element_id']}")
        print("Nodes:")
        for node in element['nodes']:
            print(f"  - ({node['x']}, {node['y']}, {node['z']})")
        print("\n")

# Test if everything works from teacher Martina: 
# spaces = model.by_type("IfcBeamType")
# for space in spaces:
#     print(space.HasPropertySets)
#AAaaa