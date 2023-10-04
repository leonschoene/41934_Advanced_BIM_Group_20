import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.selector
from pathlib import Path
import numpy as np
import math

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


# Create list with all beams 
beam_values = []

def get_beam_values():
    for beam in model.by_type('IfcBeam'):
        id = ifcopenshell.util.selector.get_element_value(beam, 'Tag')
        x = ifcopenshell.util.selector.get_element_value(beam, 'x')
        y = ifcopenshell.util.selector.get_element_value(beam, 'y')
        z = ifcopenshell.util.selector.get_element_value(beam, 'z')
        slope = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Slope')
        length = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Span')
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, beam)
        matrix = shape.transformation.matrix.data
        matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
        plane = get_beam_plane(beam)
        direction = get_direction(beam)
        beam ={
            'Tag' : id,
            'X' : x,
            'Y' : y,
            'Z' : z,
            'Slope' : slope,
            'Length' : length,
            'Matrix' : matrix,
            'Plane' : plane,
            'Direction' : direction
        }
        beam_values.append(beam)

    return beam_values

# find the plane or the direction in that the beam extend
def get_beam_plane(beam):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, beam)
    slope = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Slope')
    verts = shape.geometry.verts
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)

    # Set all max differences of points equal 0
    max_diff_x = 0
    max_diff_y = 0
    max_diff_z = 0
    max_diff_index = None

    # look for the biggest difference between nodes for each direction (x,y,z)
    for i in range(1, len(grouped_verts)):
        diff_x = abs(grouped_verts[i][0] - grouped_verts[i-1][0])
        diff_y = abs(grouped_verts[i][1] - grouped_verts[i-1][1])
        diff_z = abs(grouped_verts[i][2] - grouped_verts[i-1][2])

        if diff_x > max_diff_x:
            max_diff_x = diff_x
        if diff_y > max_diff_y:
            max_diff_y = diff_y
        if diff_z > max_diff_z:
            max_diff_z = diff_z

    # look for the maximum difference between each axis 
    max_diff_value = max(max_diff_x, max_diff_y, max_diff_z)

    if slope == 0: # a horizontal beam has no second direction, it extend only in one axis
        if max_diff_value == max_diff_x:
            plane = 'x'
        elif max_diff_value == max_diff_y:
            plane = 'y'
        else:
            plane = 'z'
        return plane
    else: # if beam has a slope, it also has a second direction that is >> third direction which is his own depth
        max_diff_list = sorted([max_diff_x, max_diff_y, max_diff_z], reverse=True) # sort the list 

        first_max_diff = max_diff_list[0]
        second_max_diff = max_diff_list[1]

        # look which direction has the biggest difference
        if first_max_diff == max_diff_x:
            first_direction = "x"
        elif first_max_diff == max_diff_y:
            first_direction = "y"
        else:
            first_direction = "z"

        # look which direction has the second biggest difference
        if second_max_diff == max_diff_x:
            second_direction = "x"
        elif second_max_diff == max_diff_y:
            second_direction = "y"
        else:
            second_direction = "z"

        # create list of the plane and sort that alphabetical, so that we get xy-, xz-, or yz-plane
        plane = [first_direction, second_direction]
    
    sorted_plane = sorted(plane)
    return sorted_plane

def get_direction(beam):
    slope = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Slope')
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, beam)
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
    rotationmatrix = matrix[:3,:3]

    if get_beam_plane == ['y','z'] or ['y'] or ['z']:
        v_lokal = np.array([[0], [math.cos(math.radians(slope))], [math.sin(math.radians(slope))]])
    elif get_beam_plane == ['x' and 'z'] or ['z']:
        v_lokal = np.array([[math.cos(math.radians(slope))], [0], [math.sin(math.radians(slope))]])
    elif get_beam_plane == ['x','y'] or ['x'] or ['y']:
        v_lokal = np.array([[math.cos(math.radians(slope))], [math.sin(math.radians(slope))], [0]])
    else:
        print('Error')

    v_global = rotationmatrix @ v_lokal

    return v_global



beams = get_beam_values()
print(beams)

with open('liste.txt', 'w') as f:
    for element in beams:
        f.write(str(element) + '\n')



# Test if everything works from teacher Martina: 
# spaces = model.by_type("IfcBeamType")
# for space in spaces:
#     print(space.HasPropertySets)
#     print(space.HasPropertySets)