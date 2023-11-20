# 41934 Advanced BIM Group 20 Assignment 4
## Role Learning Level and Focus Area
Since we are modelling and editing a model in BlenderBIM in conformance with the OpenBIM IFC standard, and adding various property sets to an IFC file using ifcOpenShell, we reached to the conclusion that the role learning level is targeted to Level 2. However, a small introduction for Level 1 is carried out.

The focus area is structural analysis.

## Use Case
Structural engineers often need a simplified structural model from an architectural IFC file. Based on this, our script calculates the start and end points of each loadbearing beam and column and they are concected by lines. The start and end point represent the nodes and the lines the elements in a simplified structural model. In addition to the start point and end point, the cross-section and material type is extracted.

Additionally, a CSV file is created with all materials that are defined in the model and the user's task is to add manually specific material properties like density, compressive strength, yield strength, and ultimate strength. The script will read the CSV file and will add the material properties from the CSV file and it will save the enriched model as a new IFC file called "updated_model.ifc".


A video showing the use case can be found on [this link.](https://external.ink?to=www.youtube.com/watch?v=qbk8SYr7DuA&list=PLWuWtXSyAvKSiMLpkFOxh2hRPt-7aHBCY&index=2)

## Level 1: Introduction
First of all, the user has to install a code editor such as "Visual Studio Code" and then install python (conda).
The libraries needed to run the script are:
* numpy
* ifcopenshell
* ifcopenshell.api
* sys
* pandas

These libraries can be installed through the command "pip". An example is shown [here](https://blenderbim.org/docs-python/ifcopenshell-python/installation.html#pypi)

## Tool description
The first part is a tool without the user's interaction. The user has to upload the IFC file to the tool and it starts to generate the coordinates for each element. The script looks then for load-bearing elements like beams and columns. In the case that the model contains no structural elements, the user gets a notification that the tool could not find any load-bearing elements and the user has to upload a new file. If there are load-bearing elements, the tool extracts the start and end points of each element and write them in a list for beams and columns. The start and end points get the script from the vertices through ifcopenshell. Once the tool has the vertices in a matrix, it looks for the direction by looking for the first and second (in the case of a sloped beam/column) biggest distance and assigns a plane to the element. The plane is important to calculate the correct direction vector that is multiplied by the rotation matrix to get the absolute coordinate of the element. By adding or subtracting the half of the length we get the start and end point for the element. Afterwards, the script extracts the cross-section and material for each element and stores it in a list. This information is also saved in the created lists. At the end of this part, the tool creates a new IFC file with the coordinates of each element and connects the nodes with lines that refer to the original element tag. This created IFC file can also now be used for other programs like a FEM software. A detailed description of this part of the tool can be found in [this link](https://www.youtube.com/watch?v=YblPnmZ72po&list=PLWuWtXSyAvKSiMLpkFOxh2hRPt-7aHBCY&index=3).

The user also has the possibility of continuing the script and add material properties to the model. The purpose of this part of the tool is to enrich the IFC model with material properties that have not been defined yet, for example, material density, material compressive strength, etc. The script goes through all elements in the model and looks for the different materials. Afterwards, a CSV file is created with all material classes that are defined in the model. The user's task is now to add manually specific material properties like density, compressive strength, yield strength, and ultimate strength. The script will read the CSV file and will add the material properties from the CSV file. A new enriched IFC file is created and stored as "updated_model.ifc". A more elaborated description of this section is presented [here](https://www.youtube.com/watch?v=KLo88A0XLcs&list=PLWuWtXSyAvKSiMLpkFOxh2hRPt-7aHBCY&index=3&pp=iAQB).

Note that in order to understand how this tool works step by step, the script has been commented thoroughly.

In order to check how the BIM tool truly works and a full demonstration of it, the reader is more than welcomed to watch [this video](https://www.youtube.com/watch?v=Q-Lz2lOV1Qg&list=PLWuWtXSyAvKSiMLpkFOxh2hRPt-7aHBCY&index=5).

## Script's limitations
* Due to the fact that the SkyLab model was used, which are not permitted to share it in public repositories, it has to be stored in a local folder, whose name should be "model" and it should be placed in the parent parent folder from the script.
* The model has to be IFC 4x.
* Through the script, some property sets can be added. However, if another property set wants to be incorporated, the script has to be modified accordingly.
* The properties added to the IFC file should be added with their proper units. Otherwise, it will end up with inconsistencies in a future FEM software analysis.
* It is important to add the properties with Excel. Otherwise, the text editor gives error because the csv file is in use and can not be saved.

## Future improvements
* Developing the script in order to consider all the bearing elements (not only beams and columns, but slabs, walls and footings).
* In order to improve the interaction process with the user, it would be nice to make the script more user-friendly through HTML.
* Improving units managment, so user can work in any desired unit system.
* Interactive plot, i.e. making it possible to move around in the plot and not just a picture of it.
* Including external loads and support conditions.
* Exporting all the data for performing a structural analysis.
