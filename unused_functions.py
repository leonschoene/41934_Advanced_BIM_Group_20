#######################################################################
#######################################################################
## storage file for all functions we don't need in the main program, ##
## but we also did't delete these function. Maybe there is a later   ##
## usecase for them.                                                 ##
#######################################################################
#######################################################################


# def get_direction(beam):
#     slope = ifcopenshell.util.selector.get_element_value(beam, 'Pset_BeamCommon.Slope')
#     settings = ifcopenshell.geom.settings()
#     shape = ifcopenshell.geom.create_shape(settings, beam)
#     matrix = shape.transformation.matrix.data
#     matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
#     rotationmatrix = matrix[:3,:3]
#     plane = get_beam_plane(beam)
#     plane_value = plane[1]
#     v_lokal = np.array([[0], [0], [0]])

#     # # Convert the plane list to a string without using a separator
#     # plane_string = plane

#     # if plane_string == "x" or plane_string == "xy":
#     #     v_lokal = np.array([[math.cos(math.radians(slope))], [math.sin(math.radians(slope))], [0]])
#     # elif plane_string == "y" or plane_string == "yz":
#     #     v_lokal = np.array([[0], [math.cos(math.radians(slope))], [math.sin(math.radians(slope))]])
#     # elif plane_string == "z" or plane_string == "xz":
#     #     v_lokal = np.array([[math.cos(math.radians(slope))], [0], [math.sin(math.radians(slope))]])
#     # else:
#     #     print('No plane founded')

#     if plane_value == 1 or plane_value == 12:
#         v_lokal = np.array([[math.cos(math.radians(slope))], [math.sin(math.radians(slope))], [0]])
#     elif plane_value == 2 or plane_value == 23:
#         v_lokal = np.array([[0], [math.cos(math.radians(slope))], [math.sin(math.radians(slope))]])
#     elif plane_value == 3 or plane_value == 13:
#         v_lokal = np.array([[math.cos(math.radians(slope))], [0], [math.sin(math.radians(slope))]])
#     else:
#         print('No plane founded')

#     v_global = rotationmatrix @ v_lokal

#    return v_global