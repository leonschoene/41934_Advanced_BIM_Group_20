import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.selector
from pathlib import Path
import numpy as np
import math
import matplotlib.pyplot as plt

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
        mesh = get_beam_coordinates(beam)
        mesh_center = get_mesh_center(mesh)
        startpoint = get_startpoint(mesh_center, length, plane[2])
        endpoint = get_endpoint(mesh_center, length, plane[2])
        beam ={
            'Tag' : id,
            'X' : x,
            'Y' : y,
            'Z' : z,
            'Slope' : slope,
            'Length' : length,
            'Matrix' : matrix,
            'Plane' : plane,
            'Mesh center' : mesh_center,
            'Startpoint' : startpoint,
            'Endpoint' : endpoint
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
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
    rotationmatrix = matrix[:3,:3]
    v_lokal = np.array([[0], [0], [0]])

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
            plane_value = 1
        elif max_diff_value == max_diff_y:
            plane = 'y'
            plane_value = 2
        else:
            plane = 'z'
            plane_value = 3
        
        if plane_value == 1 or plane_value == 12:
            v_lokal = np.array([[math.cos(math.radians(slope))], [math.sin(math.radians(slope))], [0]])
        elif plane_value == 2 or plane_value == 23:
            v_lokal = np.array([[0], [math.cos(math.radians(slope))], [math.sin(math.radians(slope))]])
        elif plane_value == 3 or plane_value == 13:
            v_lokal = np.array([[math.cos(math.radians(slope))], [0], [math.sin(math.radians(slope))]])
        else:
            print('No plane founded')

        v_global = rotationmatrix @ v_lokal
        return (plane, plane_value, v_global)
    
    else: # if beam has a slope, it also has a second direction that is >> third direction which is his own depth
        max_diff_list = sorted([max_diff_x, max_diff_y, max_diff_z], reverse=True) # sort the list 

        first_max_diff = max_diff_list[0]
        second_max_diff = max_diff_list[1]

        # look which direction has the biggest difference
        if first_max_diff == max_diff_x:
            first_direction = "x"
            first_plane_value = 1
        elif first_max_diff == max_diff_y:
            first_direction = "y"
            first_plane_value = 2
        else:
            first_direction = "z"
            first_plane_value = 3

        # look which direction has the second biggest difference
        if second_max_diff == max_diff_x:
            second_direction = "x"
            second_plane_value = 2
        elif second_max_diff == max_diff_y:
            second_direction = "y"
            second_plane_value = 2
        else:
            second_direction = "z"
            second_plane_value = 3
        
        # create list of the plane and sort that alphabetical, so that we get xy-, xz-, or yz-plane
        plane = [first_direction,second_direction]
        plane_value = [first_plane_value,second_plane_value]
        sorted_plane_value = sorted(plane_value)
        sorted_plane_value = list(map(str, sorted_plane_value))
        plane_value = int("".join(sorted_plane_value))

    if plane_value == 1 or plane_value == 12:
        v_lokal = np.array([[math.cos(math.radians(slope))], [math.sin(math.radians(slope))], [0]])
    elif plane_value == 2 or plane_value == 23:
        v_lokal = np.array([[0], [math.cos(math.radians(slope))], [math.sin(math.radians(slope))]])
    elif plane_value == 3 or plane_value == 13:
        v_lokal = np.array([[math.cos(math.radians(slope))], [0], [math.sin(math.radians(slope))]])
    else:
        print('No plane founded')

    v_global = rotationmatrix @ v_lokal

    sorted_plane = sorted(plane)
    return (sorted_plane, plane_value, v_global)


def get_coordinates(beam):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, beam)
    verts = shape.geometry.verts
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)

    vertices = []
    for shell in beam.get_open_shells():
        for vertex in shell.get_vertices():
            vertices.append(vertex.get_coordinates())

    mesh = np.array(vertices)
    v = np.array([vertices[0],vertices[1],vertices[2],1])

    v_abs = matrix @ v
    v_abs = np.array([v_abs[0],v_abs[1],v_abs[2]])

    return v_abs


def get_beam_coordinates(beam):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, beam)
    verts = shape.geometry.verts
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)

    # put grouped verts in np.array
    grouped_verts = np.array(grouped_verts)
    # insert '1' to each axis 
    mesh = np.insert(grouped_verts,3,1, axis=1)
    # multily the mesh with the original matrix (rotation and position)
    mesh_abs = mesh @ matrix.T
    # delete the last column of each axis
    mesh_abs = np.take(mesh_abs, [0, 1, 2], axis=1)

    return mesh_abs


def get_mesh_center(mesh):
    # Calculate the mean of the mesh coordinates
    mesh_center = np.mean(mesh, axis=0)

    return mesh_center

def get_startpoint(mesh_center, length, direction):
    # Calculate the startpoint from the beam
    sp = mesh_center - length/2000*direction.T

    return sp

def get_endpoint(mesh_center, length, direction):
    # Calculate the startpoint from the beam
    ep = mesh_center + length/2000*direction.T

    return ep
    
#####################################################################
# Code for the entire model, store values for all beams in the list #
#####################################################################

# Get list over searching for plane
beams = get_beam_values()

with open('liste.txt', 'w') as f:
    for element in beams:
        f.write(str(element) + '\n')

print('List with all beams is create and safed to liste.txt')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Iterate over list beam_values and plot lines between start- and endpunkt
for element in beam_values:
    sp = element['Startpoint']
    ep = element['Endpoint']

    if sp.shape == (1, 3) and ep.shape == (1, 3):
        x_start, y_start, z_start = sp[0]
        x_end, y_end, z_end = ep[0]

        # Plot lines between start- and endpunkt
        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], marker='o')
    
    else:
        print('Beam has no correct array')
        print(len(sp), len(ep))

# optinal titles
ax.set_xlabel('X-Achse')
ax.set_ylabel('Y-Achse')
ax.set_zlabel('Z-Achse')
ax.set_title('3D Plot of start- and endpoints')

# Show 3D-Plot
plt.show()

####################################
# Code for one element for testing #
####################################

# beam = model.by_type('IfcBeam')[2]
# print('Tag:', beam.Tag)
# beam_coordinates = get_beam_coordinates(beam)
# mesh = get_beam_coordinates(beam)

# # Calculate the mesh center
# mesh_center = get_mesh_center(mesh)

# # Get the x, y, and z coordinates of the beam
# x = beam_coordinates[:, 0]
# y = beam_coordinates[:, 1]
# z = beam_coordinates[:, 2].reshape(-1, 1)

# # Plot the beam in 3D
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(x, y, z)
# #ax.set_aspect('equal')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# # Plot the mesh center
# ax.plot(mesh_center[0], mesh_center[1], mesh_center[2], 'b*')

# # Show the plot
# plt.show()

# print(mesh_center)

##################################################
# Test if everything works from teacher Martina: #
##################################################

# spaces = model.by_type("IfcBeamType")
# for space in spaces:
#     print(space.HasPropertySets)
#     print(space.HasPropertySets)