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
# First part: count elements 
beams = model.by_type('IfcBeam')
columns = model.by_type('IfcColumn')
slab = model.by_type('IfcSlab')

print('beams: ', len(beams))
print('columns: ', columns)
print('slab: ', len(slab))



# Test if everything works from teacher Martina: 
spaces = model.by_type("IfcBeamType")
for space in spaces:
    print(space.HasPropertySets)
