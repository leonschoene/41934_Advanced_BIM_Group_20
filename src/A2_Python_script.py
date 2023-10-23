import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.selector
import os
from pathlib import Path
import numpy as np
import math
import matplotlib.pyplot as plt

modelname = "LLYN - STRU"

# Code from teacher Martina for testing
try:
    dir_path = Path(__file__).parent.parent
    model_rel_path = os.path.join('..', 'model', modelname + '.ifc')
    model_url = dir_path.joinpath(model_rel_path)
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



#2. part: Create lists and get their values
beam_values = []
column_values = []
material_list = []

def get_beam_values():
    for beam in model.by_type('IfcBeam'):
        id = ifcopenshell.util.selector.get_element_value(beam, 'Tag')
        x = ifcopenshell.util.selector.get_element_value(beam, 'x')
        y = ifcopenshell.util.selector.get_element_value(beam, 'y')
        z = ifcopenshell.util.selector.get_element_value(beam, 'z')
        crosssection = ifcopenshell.util.selector.get_element_value(beam, 'Pset_ReinforcementBarPitchOfBeam.Description')
        material = beam.HasAssociations[0].RelatingMaterial.Name
        slope = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Slope')
        length = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Span')
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, beam)
        matrix = shape.transformation.matrix.data
        matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
        plane = get_beam_plane(beam)
        mesh = get_element_coordinates(beam)
        mesh_center = get_mesh_center(mesh)
        startpoint = get_startpoint_beam(mesh_center, length, plane[2])
        endpoint = get_endpoint_beam(mesh_center, length, plane[2])
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
            'Endpoint' : endpoint,
            'Cross-Section' :  crosssection,
            'Material' : material
        }
        beam_values.append(beam)

    return beam_values

def get_column_values():
    for column in model.by_type('IfcColumn'):
        id = ifcopenshell.util.selector.get_element_value(column, 'Tag')
        x = ifcopenshell.util.selector.get_element_value(column, 'x')
        y = ifcopenshell.util.selector.get_element_value(column, 'y')
        z = ifcopenshell.util.selector.get_element_value(column, 'z')
        crosssection = ifcopenshell.util.selector.get_element_value(column, 'Pset_ReinforcementBarPitchOfColumn.Description')
        material = column.HasAssociations[0].RelatingMaterial.Name
        slope = ifcopenshell.util.selector.get_element_value(column, 'Pset_ColumnCommon.Slope')
        length = ifcopenshell.util.selector.get_element_value(column, 'Qto_ColumnBaseQuantities.Span')
        settings = ifcopenshell.geom.settings()
        shape = ifcopenshell.geom.create_shape(settings, column)
        matrix = shape.transformation.matrix.data
        matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
        plane = get_column_plane(column)
        mesh = get_element_coordinates(column)
        mesh_center = get_mesh_center(mesh)
        startpoint = get_startpoint_col(mesh_center, plane[3], plane[2])
        endpoint = get_endpoint_col(mesh_center, plane[3], plane[2])
        column ={
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
            'Endpoint' : endpoint,
            'Cross-section' : crosssection,
            'Material' : material
        }
        column_values.append(column)

    return column_values

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
            print('Element Tag:', beam.Tag)

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
        print('Element Tag:', beam.Tag)
        

    v_global = rotationmatrix @ v_lokal

    sorted_plane = sorted(plane)
    return (sorted_plane, plane_value, v_global)

# find the plane or the direction in that the column extend
def get_column_plane(column):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, column)
    slope = ifcopenshell.util.selector.get_element_value(column, 'Pset_ColumnCommon.Slope')
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
    length = max_diff_value

    if slope == None:
        plane = 'z'
        plane_value = 3
        v_lokal = np.array([[0], [0], [1]])

        v_global = rotationmatrix @ v_lokal # global direction vector
        return (plane, plane_value, v_global, length)

    elif slope == 0: # a horizontal beam has no second direction, it extend only in one axis
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
            print('Element Tag:', column.Tag)

        v_global = rotationmatrix @ v_lokal
        return (plane, plane_value, v_global, length)
    
    else: # if column has a slope, it also has a second direction that is >> third direction which is his own depth
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
        print('Element Tag:', column.Tag)
        

    v_global = rotationmatrix @ v_lokal

    sorted_plane = sorted(plane)
    return (sorted_plane, plane_value, v_global, length)


def get_coordinates(element):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, element)
    verts = shape.geometry.verts
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)

    vertices = []
    for shell in element.get_open_shells():
        for vertex in shell.get_vertices():
            vertices.append(vertex.get_coordinates())

    mesh = np.array(vertices)
    v = np.array([vertices[0],vertices[1],vertices[2],1])

    v_abs = matrix @ v
    v_abs = np.array([v_abs[0],v_abs[1],v_abs[2]])

    return v_abs


def get_element_coordinates(element):
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, element)
    verts = shape.geometry.verts
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    matrix = shape.transformation.matrix.data
    matrix = ifcopenshell.util.shape.get_shape_matrix(shape)

    # put grouped verts in np.array
    grouped_verts = np.array(grouped_verts)
    # insert '1' to each axis 
    mesh = np.insert(grouped_verts,3,1, axis=1)
    # multiply the mesh with the original matrix (rotation and position)
    mesh_abs = mesh @ matrix.T
    # delete the last column of each axis
    mesh_abs = np.take(mesh_abs, [0, 1, 2], axis=1)

    return mesh_abs


def get_mesh_center(mesh):
    # Calculate the mean of the mesh coordinates
    mesh_center = np.mean(mesh, axis=0)

    return mesh_center

def get_startpoint_beam(mesh_center, length, direction):
    # Calculate the startpoint from the beam
    sp_beam = mesh_center - length/2000*direction.T

    return sp_beam

def get_endpoint_beam(mesh_center, length, direction):
    # Calculate the startpoint from the beam
    ep_beam = mesh_center + length/2000*direction.T

    return ep_beam

def get_startpoint_col(mesh_center, length, direction):
    # Calculate the startpoint from the column
    sp_col = mesh_center - length/2*direction.T

    return sp_col

def get_endpoint_col(mesh_center, length, direction):
    # Calculate the startpoint from the column
    ep_col = mesh_center + length/2*direction.T

    return ep_col

def get_material():
    for element in model.by_type('IfcBeam'):
        material = element.HasAssociations[0].RelatingMaterial.Name
        print(material)
        if material not in material_list:
            material_list.append(material)

    for element in model.by_type('IfcColumn'):
        material = element.HasAssociations[0].RelatingMaterial.Name
        print(material)
        if material not in material_list:
            material_list.append(material)

    return material_list



#####################################################################
# Code for the entire model, store values for all beams in the list #
#####################################################################

# Get list over searching for plane
beams = get_beam_values()
columns = get_column_values()
materials = get_material()

with open(os.path.join(Path(__file__).parent, '..', 'results', 'list_beams.txt'), 'w') as f:
    for element in beams:
        f.write(str(element) + '\n')

print('List with all beams was created and safed to list_beams.txt')

with open(os.path.join(Path(__file__).parent, '..', 'results', 'list_columns.txt'), 'w') as f:
    for element in columns:
        f.write(str(element) + '\n')

print('List with all columns was created and safed to list_columns.txt')

with open(os.path.join(Path(__file__).parent, '..', 'results', 'materials.txt'), 'w') as f:
    for element in materials:
        f.write(str(element) + '\n')

print('List with all materials was created and safed to materials.txt')

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

# Iterate over list column_values and plot lines between start- and endpunkt
for element in column_values:
    sp = element['Startpoint']
    ep = element['Endpoint']

    if sp.shape == (1, 3) and ep.shape == (1, 3):
        x_start, y_start, z_start = sp[0]
        x_end, y_end, z_end = ep[0]

        # Plot lines between start- and endpunkt
        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end], marker='o')
    
    else:
        print('Column has no correct array')
        print(len(sp), len(ep))

# optinal titles
ax.set_xlabel('X-Axis')
ax.set_ylabel('Y-Axis')
ax.set_zlabel('Z-Axis')
ax.set_title('3D Plot of start- and endpoints')

# Show 3D-Plot
plt.show()

####################################
# Code for one element for testing #
####################################

# column = model.by_guid('2Bbtc4Qtb4v9USChXqpW23')#[2]
# plane = get_column_plane(column)
# print(plane[3])
# print(column.Tag)

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