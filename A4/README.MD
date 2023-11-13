# 41934 Advanced BIM Group 20 Assignment 4
## Role Learning Level and Focus Area
Since we are modelling and editing a model in BlenderBIM in conformance with the OpenBIM IFC standard, and adding various property sets to an IFC file using ifcOpenShell, we reached to the conclusion that the role learning level is targeted to Level 2. However, a small introduction for Level 1 is carried out

The focus area is structural analysis.

## Use Case
Structural engineers often need a simplified structural model from an architectural IFC file. Based on this, our script calculates the start and end points of each loadbearing beam and column and they are concected by lines. The start and end point represent the nodes and the lines the elements in a simplified structural model. In addition to the start point and end point, the cross-section and material type is extracted.

Additionally, a CSV file is created with all materials that are defined in the model and the user's task is to add manually specific material properties like density, compressive strength, yield strength, and ultimate strength. The script will read the CSV file and will add the material properties from the CSV file and it will save the enriched model as a new IFC file called "updated_model.ifc".


A video showing the use case can be found on this link. (REMEMBER TO ATTACH LINK)

## Level 1: Introduction
The libraries needed to run the script are:
* numpy
* ifcopenshell
* ifcopenshell.api
* sys
* pandas

### Limitations
Due to the fact that the SkyLab model was used, which are not permitted to share it in public repositories, it has to be stored in a local folder, which name should be "model" and should be placed in the parent parent folder from the script.
