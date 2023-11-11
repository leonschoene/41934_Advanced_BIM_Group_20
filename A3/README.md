# Report
## 3A: Analyse use case
### 1. Goal
Add material properties, e.g. the density, compressive strength, and yield strength to each element in the IFC model to calculate e.g. weight and dead load for each element.
### 2. Model Use (BIM use)
![BEP](BEP.md)
## 3B: Propose a (design for a) tool / workflow
### 1. Process: 
![BPMN Use Case](BPMN_Group_20_A3.svg)
The BPMN diagram shows the entire design for a BIM use case, the assignment 3 includes only the red box which is described in the following section.
### 2. Description:
The purpose of this use case is to add material properties to the IFC file that are not existing before. The script goes through all elements in the model and looks for the material. In the end the script creates a CSV file with all materials that are used in the model. The user's task is now to add manually specific material properties like density, compressive strength, and yield strength and save the file. 
Now, the user must go back to the command line in his coding environment and continue the script by pressing Y and confirm with Enter. 
The script will read the CSV file and go through each element and add the material properties from the CSV file and will save the enriched model as a new IFC file called "updated_model.ifc".
## 3C [removed for this assignment]
## 3D: Value: What is the potential improvement offered by this tool?
The tool will save a huge amout of time of an employer. In the past the material properties have to be added by hand for each element in BlenderBIM. With this tool it just needs a couple of seconds to add several properties to all elements in the model.
The tool will not make the world directly to a better place in terms of peace, but it will save time by speeding up the planning process and save a lot of money.
