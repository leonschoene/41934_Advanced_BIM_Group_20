# BIM Execution Plan
![BPMN Diagram](BPMN_Group_20_A3.svg)
## Goal
The tool should create a structural analysis report. That will be achieved by retrieve an IFC file from e.g. the architect and upload that to the tool. The tool will then run through various steps and the user has to interact with it on one point.
## Model Uses
### What does the setup?
#### 1. Create CSV file with coordinates
The first part is a tool without the user's interaction. The user has to upload the IFC file to the tool and the tool starts to generate the coordinates for each element. 
The script looks then for load bearing elements like beams and columns. In the case that the model contains no structural elements, the user gets a notification that the tool could not find any load bearing elements and the user has to upload a new file. If there are load bearing elements the tool extracts the start and end points of each element and write it to a list for beams and columns. The start and end points get the script from the vertices through ifcopenshell. Once the tool has the vertices in a matrix, it looks for the direction by looking for the first and second (in the case of a sloped beam/column) biggest distance and assigns a plane to the element. Afterwards, the script extract the cross section and material for each element and stored it to a list in the tool. These information are also saved in the created lists. 
At the end of this part the tool creates a new IFC file with the coordinates of each element and connects the nodes with lines which are refered to the original element tag. This created IFC file can also now used for other programs like a FEM software or the user continues the script and add material properties to the model which is described in th next section. 
#### 2. Add material properties
#### 3. Add different loads
The user has here the possibility to upload data for external loads like wind, seismic, a snow loads and upload the support conditions of the model. 
#### 4. Strucutral analysis
### Who will use it


