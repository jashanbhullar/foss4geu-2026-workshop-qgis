# QGIS Model Workflow

## Goal

Build a QGIS 3 Processing model that follows the same logic as the manual workflow:

- Clip first in source CRS.
- Reproject only the final clipped output.
- For raster, choose bands at the end.

The model must let the user:

- Select an AOI polygon layer.
- Choose either vector or raster processing.
- Select raster bands when raster mode is used.
- Choose final output CRS.
- Provide final output name/path.

## Model Inputs

Create these parameters in Model Designer:

1. AOI polygon layer
   - Type: Vector Layer (Polygon)
   - Name: AOI
2. Processing mode
   - Type: Enum
   - Options: Vector, Raster
   - Name: Processing_Mode
3. Vector input
   - Type: Vector Layer (Any geometry)
   - Name: Vector_Input
4. Raster input
   - Type: Raster Layer
   - Name: Raster_Input
5. Raster bands
   - Type: String (comma-separated list)
   - Default: 1,2,3
   - Name: Raster_Bands
6. Target CRS
   - Type: CRS
   - Default: EPSG:8857
   - Name: Target_CRS
7. Final vector output
   - Type: Vector Destination
   - Name: Final_Vector_Output
8. Final raster output
   - Type: Raster Destination
   - Name: Final_Raster_Output

Use preconditions so only the selected branch runs:

- Vector branch runs when Processing_Mode = Vector.
- Raster branch runs when Processing_Mode = Raster.

## Step-by-Step in QGIS Model Designer

1. Open Model Designer
    - Processing > Graphical Modeler.
    - Click New Model.
    - Set Name: AOI Vector Raster Workflow.
    - Set Group: Workshop (or your preferred group).

2. Add model input parameters
    - In the Inputs panel, add Parameter Vector Layer:
       - Description: AOI
       - Geometry type: Polygon
    - Add Parameter Enum:
       - Description: Processing_Mode
       - Options: Vector,Raster
       - Default: Vector
    - Add Parameter Vector Layer:
       - Description: Vector_Input
       - Geometry type: Any
    - Add Parameter Raster Layer:
       - Description: Raster_Input
    - Add Parameter Raster Band:
       - Description: Raster_Bands
       - Default: 1,2,3
    - Add Parameter CRS:
       - Description: Target_CRS
       - Default: EPSG:8857
    - Add Conditional Branch:
       - Description: Vector Branch
    - Add Conditional Branch:
       - Description: Raster Branch

3. Build the vector branch
    - Add algorithm native:clip.
       - Input layer: Vector_Input
       - Overlay layer: AOI
    - Add algorithm native:reprojectlayer.
       - Input layer: output of clip
       - Target CRS: Target_CRS
       - Reprojected: Final_Vector_Output
    - Open each vector algorithm and set precondition:
       - Processing_Mode equals Vector.

4. Build the raster branch
    - Add algorithm gdal:cliprasterbymasklayer.
       - Input layer: Raster_Input
       - Mask layer: AOI
       - Match extent to mask layer: enabled
    - Add algorithm gdal:rearrange_bands.
       - Input layer: output of warp
       - Selected bands: Raster_Bands
       - Output: Final_Raster_Output
    - Open each raster algorithm and set precondition:
       - Processing_Mode equals Raster.

5. Mark outputs clearly
    - Confirm only these are final model outputs:
       - Final_Vector_Output
       - Final_Raster_Output
    - Leave all other branch results as intermediate outputs.

6. Save and test the model
    - Save model as a .model3 file.
    - Run once in Vector mode (AOI + Vector_Input + Target_CRS + Final_Vector_Output).
    - Run once in Raster mode (AOI + Raster_Input + Raster_Bands + Target_CRS + Final_Raster_Output).
    - Confirm output naming prompt appears and branch behavior is correct.

## Workflow Steps

1. Vector branch (same order as manual)
   - Run Clip:
     - Input layer: Vector_Input
     - Overlay: AOI
   - Run Reproject layer on clipped result:
     - Target CRS: Target_CRS
   - Connect this as Final_Vector_Output.

2. Raster branch (same order as manual)
   - Run Clip raster by mask layer:
     - Input raster: Raster_Input
     - Mask layer: AOI
     - Match extent to mask: enabled
   - Run Warp (reproject) on clipped raster:
     - Target CRS: Target_CRS
   - Run Rearrange bands as last step:
     - Input raster: warped clipped raster
     - Bands: Raster_Bands
   - Connect this as Final_Raster_Output.

## Output Naming

Set final names through destination parameters at run time:

- In vector mode, user sets Final_Vector_Output file name/path.
- In raster mode, user sets Final_Raster_Output file name/path.

This satisfies the final output naming requirement without hardcoded file names in the model.

## Validation Checklist

1. Vector run test
   - Select AOI + vector layer + mode Vector.
   - Confirm output is clipped and in Target_CRS.
2. Raster run test
   - Select AOI + raster layer + mode Raster.
   - Set Raster_Bands (example: 1,2,3).
   - Confirm output is clipped, reprojected, and contains selected bands only.
3. Branch check
   - Confirm non-selected branch does not execute.

## Bonus: Use a Custom Python Script in Model Designer

This section shows how to include a custom Processing script as a validation step in the same model.

Reference script:

- validation_demo.py
- Algorithm class: CheckNameField
- Behavior: validates that input vector layer has a field named name

### A. Register the script in QGIS Processing

1. Open Processing Toolbox.
2. Go to Processing > Options > Scripts.
3. Add the folder that contains validation_demo.py to Script folders.
4. Click OK.
5. In Processing Toolbox, search for Check if "name" field exists under Custom scripts.

### B. Add the script into the model

1. Open your model in Graphical Modeler.
2. In Algorithms panel, search for Check if "name" field exists.
3. Drag it into the model canvas.
4. Connect its INPUT to the vector layer you want to validate:
   - Usually Vector_Input if validating before clip.
   - Or clipped vector output if validating after clip.
5. Set branch condition so this step runs only in vector mode.

### C. Suggested placement in current workflow

For this model, place the custom validation in the vector branch before native:clip:

1. Processing_Mode = Vector
2. Check if "name" field exists (custom script)
3. native:clip
4. native:reprojectlayer

### D. What happens at run time

1. If the field name exists, the model continues normally.
2. If the field name is missing, the custom script raises a Processing error.
3. The vector branch stops and the user gets a clear validation message.

### E. Workshop tip

Use this as a simple example of where custom scripting adds value to Model Designer:

- Keep most steps low-code with built-in algorithms.
- Insert a small Python validation step only where business rules are needed.
