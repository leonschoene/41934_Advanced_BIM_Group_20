# 41934 Advanced BIM Group 20 Assignment 2
We are both studying civil engineering, so we chose the structural focus area and the structural IFC model for this assignment. 
## Use Case
Structural engineers need a simplified structural model. For that, our script calculate the start and end points of each loadbearing beam and column. Following, a point cloud out of start and end point is created and concected by lines. The start and end point represent the nodes and the lines the elements in a simplified structural model. That model can then be exported for other FEM softwares. 
### Who is the use case for?
The use case is made for engineers, but also architects who need a simplified structural model.
### What disciplinary (non BIM) expertise did you use to solve the use case?
We used vector analysis to create the start and end points out of a mesh from vertices for each element.
### What IFC concepts did you use in your script (or would you use in the rest of the tool)?
The script uses mainly ifcopenshell.
### What disciplinary analysis does it require?
It needs advanced mathematics like vector analysis and also required Python skills that are non civil engineering.
### What building elements are you interested in?
We are mainly interested in load bearing elements, in this case especially beam and columns.
### What (use cases) need to be done before you can start your use case?
There is no other use case need to be done before, you just need an IFC-file in an additional folder called model.
### What is the input data for your use case?
The input data for the use case is the model as an IFC-file.
### What other use cases are waiting for your use case to complete?
Afterwards, it would be nice to have a use case for a structural analysis, to substitute closed software through open software. 