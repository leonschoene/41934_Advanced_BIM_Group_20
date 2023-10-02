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
# only for elements if load bearing is set to true?
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
# if __name__ == '__main__':
#     elements = assign_nodes_to_elements(model)


# Erstelle eine Liste, in der die Koordinaten jedes Beams gespeichert werden
coordinates = []

#Version 1
# Gehe durch alle Beams in der IFC4-Datei
# for beam in model.by_type("IfcBeam"):

#     # Hole die Position des Anfangspunkts des Beams
#     start_point = beam.ObjectPlacement.RelativePlacement.Location

#     # Hole die Position des Endpunkts des Beams
#     end_point = beam.ObjectPlacement.RelativePlacement.RefDirection

#     # Wenn die Position des Endpunkts nicht `None` ist, dann füge sie der Liste hinzu
#     if end_point is not None:
#         coordinates.append((beam.Tag, start_point.Coordinates[0], start_point.Coordinates[1], start_point.Coordinates[2], end_point.DirectionRatios[0], end_point.DirectionRatios[1], end_point.DirectionRatios[2]))

# print(coordinates)

#Version 2
# Gehe durch alle Beams in der IFC4-Datei
# for beam in model.by_type("IfcBeam"):

#     # Hole die Position des middlepoint des Beams
#     middle_point = beam.ObjectPlacement.RelativePlacement.Location


#     # Wenn die Position des Endpunkts nicht `None` ist, dann füge sie der Liste hinzu
#     coordinates.append((beam.Tag, middle_point.Coordinates[0], middle_point.Coordinates[1], middle_point.Coordinates[2]))

# print(coordinates)

#Version 3
# Gehe durch alle Beams in der IFC4-Datei
for beam in model.by_type("IfcBeam"):

    # Hole das Property Set des Beams
    property_set = model.get_property_set_by_name("IfcBeamStandardCase")

    # Hole die Länge aus dem Property Set
    length = property_set.get("Length")

    # Hole die Position des Beams
    position = beam.Position

    # Hole den Mittelpunkt des Beams
    mid_point = position.Location

    # Füge den Mittelpunkt und die Länge der Liste hinzu
    coordinates.append((beam.Tag, mid_point.Coordinates[0], mid_point.Coordinates[1], mid_point.Coordinates[2], length))

print(coordinates)

# Test if everything works from teacher Martina: 
# spaces = model.by_type("IfcBeamType")
# for space in spaces:
#     print(space.HasPropertySets)