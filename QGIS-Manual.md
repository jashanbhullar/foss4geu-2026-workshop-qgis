# Manual QGIS Workflow

## Objective

Demo data package:

- Download the workshop sample data from <https://drive.google.com/file/d/1WvRVhR0BgKlhZuF5ebjVwKEUphy8UP8u/view?usp=sharing>
- Use the downloaded layers as the starting inputs for this workflow.

Starting layers in QGIS (all currently in EPSG:4326):

- Greater London Boundary (AOI)
- OSM London Points
- OSM London Lines
- OSM London Polygons
- London Sentinel 2 Raster with bands B1 to B12

Create 4 outputs in EPSG:8857:

1. OSM Points inside AOI
2. OSM Lines inside AOI
3. OSM Polygons inside AOI
4. Sentinel RGB raster clipped to AOI using B1 as Red, B2 as Green, B3 as Blue

## Part A - Prepare Project (Clip First)

1. Open QGIS and load all layers.
2. Keep layers in their source CRS (EPSG:4326) for clipping.
3. Optional for display consistency: set Project CRS to EPSG:4326.

Use the original Greater London Boundary layer as AOI for all clipping steps.

## Part B - Vector Outputs (Points, Lines, Polygons)

### Output 1: OSM Points inside AOI (EPSG:8857)

1. Clip points with AOI in EPSG:4326:
   - Processing Toolbox > Clip
   - Input layer: OSM London Points
   - Overlay layer: Greater London Boundary
   - Output: OSM_London_Points_AOI_4326.gpkg
2. Reproject final clipped points to EPSG:8857:
   - Processing Toolbox > Reproject layer
   - Input: OSM_London_Points_AOI_4326
   - Target CRS: EPSG:8857
   - Output: OSM_London_Points_AOI_8857.gpkg

### Output 2: OSM Lines inside AOI (EPSG:8857)

1. Clip lines with AOI in EPSG:4326:
   - Processing Toolbox > Clip
   - Input layer: OSM London Lines
   - Overlay layer: Greater London Boundary
   - Output: OSM_London_Lines_AOI_4326.gpkg
2. Reproject final clipped lines to EPSG:8857:
   - Processing Toolbox > Reproject layer
   - Input: OSM_London_Lines_AOI_4326
   - Target CRS: EPSG:8857
   - Output: OSM_London_Lines_AOI_8857.gpkg

### Output 3: OSM Polygons inside AOI (EPSG:8857)

1. Clip polygons with AOI in EPSG:4326:
   - Processing Toolbox > Clip
   - Input layer: OSM London Polygons
   - Overlay layer: Greater London Boundary
   - Output: OSM_London_Polygons_AOI_4326.gpkg
2. Reproject final clipped polygons to EPSG:8857:
   - Processing Toolbox > Reproject layer
   - Input: OSM_London_Polygons_AOI_4326
   - Target CRS: EPSG:8857
   - Output: OSM_London_Polygons_AOI_8857.gpkg

## Part C - Raster Output (Sentinel RGB B1/B2/B3)

### Output 4: Sentinel RGB clipped to AOI (EPSG:8857)

1. Clip source raster by AOI in EPSG:4326:
   - Processing Toolbox > Clip raster by mask layer
   - Input layer: London Sentinel 2 raster
   - Mask layer: Greater London Boundary
   - Match extent to mask layer: checked
   - Keep resolution: checked (or set explicit resolution if needed)
   - Output: Sentinel_AOI_4326.tif

2. Reproject clipped raster to EPSG:8857:
   - Processing Toolbox > Warp (reproject)
   - Input layer: Sentinel_AOI_4326.tif
   - Target CRS: EPSG:8857
   - Resampling method: Bilinear (or Nearest if required)
   - Output: Sentinel_AOI_8857.tif

3. Build the final 3-band raster with B1, B2, B3 (last step):
   - Processing Toolbox > Rearrange (Convert format)
   - Input layer: Sentinel_AOI_8857.tif
   - Data type: keep source or set Float32
   - In Band selection, include only bands 1, 2, 3 (B1, B2, B3)
   - Output: Sentinel_B1B2B3_AOI_8857.tif

4. Set RGB rendering:
   - Right-click Sentinel_B1B2B3_AOI_8857 > Properties > Symbology
   - Render type: Multiband color
   - Red band: 1 (B1)
   - Green band: 2 (B2)
   - Blue band: 3 (B3)
   - Click Apply and OK

## Final Checks

1. Verify each output layer CRS is EPSG:8857:
   - Right-click layer > Properties > Information
2. Confirm vector outputs are spatially inside AOI boundary.
3. Confirm raster output is clipped exactly to AOI and displays as RGB (B1/B2/B3).
4. Optional cleanup: remove or archive intermediate *_4326 layers/files.
