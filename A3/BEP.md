# BIM Execution Plan
![BPMN Diagram](BPMN_Group_20_A3.svg)
## Goal
The tool should create a structural analysis report. That will be achieved by retrieve an IFC file from e.g. the architect and upload that to the tool. The tool will then run through various steps and the user has to interact with it on one point.
## Model Uses
### What does the setup?
#### 1. Create CSV file with coordinates
The first part is a tool without the user's interaction. The user has to upload the IFC file to the tool and the tool starts to generate the coordinates for each element. 
The script looks then for load bearing elements like beams and columns. In the case that the model contains no structural elements, the user gets a notification that the tool could not find any load bearing elements and the user has to upload a new file. If there are load bearing elements the tool extracts the start and end points of each element and write it to a list for beams and columns. The start and end points get the script from the vertices through ifcopenshell. Once the tool has the vertices in a matrix, it looks for the direction by looking for the first and second (in the case of a sloped beam/column) biggest distance and assigns a plane to the element. Afterwards, the script extract the cross section and material for each element and stored it to a list in the tool. These information are also saved in the created lists. 
At the end of this part the tool creates a new IFC file with the coordinates of each element and connects the nodes with lines which are refered to the original element tag. This created IFC file can also now used for other programs like a FEM software or the user continues the script and add material properties to the model which is described in the next section. 
#### 2. Add material properties
The purpose of this part of the tool is to add material properties to the IFC file that have not been defined yet, for example, material density, material compresive strength, etc. The script goes through all elements in the model and looks for the different materials. Afterwards, a CSV file is created with all materials that are defined in the model. The user's task is now to add manually specific material properties like density, compressive strength, yield strength and ultimate strength. The script will read the CSV file and will add the material properties from the CSV file and it will save the enriched model as a new IFC file called "updated_model.ifc".
#### 3. Add different loads
The user has here the possibility to update data for external loads like wind, seismic, a snow loads and upload the support conditions for the model. The IFC model is now fully prepared to perform a structural analysis in the next part.
#### 4. Structural analysis
Considering all the previous steps, all the data should be gathered in order to perform a structural analysis. Finally, a structural report can be created. Based on this final report, different modification can be carried out in order to improve the structural design. Then, the tool starts again with these potential improvements.
### Who will use it
The tool can be used from architects to see if the designed structure can be build. But the main user should be an engineer to perform a structural analysis in less time. 
## Process
Before using the tool it is important that the person who gives you the IFC file exported an IFC4 file. Otherwise, the code is not able to run because the commands in ifcopenshell are different for IFC2x3 and IFC4. 
The person who uses the tool afterward should check if the code works also for his or her project. The code we wrote is especially for beams and columns and also works for that.
The setup is not tested for slabs, foundations, or other structural elements.
The information is written into a report that can be used to get a permit from authorities or as a readable version for persons that do not rely on the topic, e.g. various customers.
The process can be iterative. In the beginning, there must be load-bearing elements before the tool starts. In the end, before the report is created, the user has to prove, that the results are acceptable.
## Information Exchange
The minimum level of detail for our workflow to work is LOD 300, in which specific elements are confirmed as 3D object geometry with object dimensions, capacities, and connections defined. In this way, the start and end coordinate for each element can be obtained. After the workflow, the LOD will still be 300, but some additional material properties will be available for next stages.
The detailed specification of the information exchange requirements can be found in the attached [Excel-file](./ExchangeInformation.xlsx)
