# QGIS Plugin Workflow

## Goal

Demo data package:

- Download the workshop sample data from <https://drive.google.com/file/d/1WvRVhR0BgKlhZuF5ebjVwKEUphy8UP8u/view?usp=sharing>
- Load those layers into QGIS before opening the plugin so the AOI and input layer choices are available.

Build a simple workshop plugin in ./processing_demo named processing_demo.

The plugin must:

- Let the user select an AOI polygon.
- Let the user select an output CRS.
- Let the user select another layer to process (vector or raster).
- Show basic details based on selected layer type.
- If raster is selected, allow band selection.
- Let the user choose output as temporary layer or saved file.

The processing order must match the manual workflow:

- Clip first.
- Reproject the clipped result as the final reprojection.
- For raster, band selection is the last step.

## Tooling Used

1. Plugin Builder 3
   - Used to generate the initial plugin template in ./processing_demo.
2. Plugin Reloader
   - Used inside QGIS to reload plugin changes quickly during development.

## Plugin Structure

- ./processing_demo/processing_demo.py
  - Plugin entry point and workflow execution.
- ./processing_demo/processing_demo_dialog.py
  - Simple UI and input validation.
- ./processing_demo/processing_demo_dialog_base_ui.py
  - Base UI layout for the dialog widgets.
- ./processing_demo/metadata.txt
  - Plugin metadata for QGIS.
- ./processing_demo/README.md
  - Developer instructions for setup and iteration.

## Step-by-Step Build Process

1. Start from the existing Plugin Builder 3 scaffold in ./processing_demo.
2. Keep the plugin class name and menu label as processing_demo.
3. Implement the base layout in processing_demo_dialog_base_ui.py with:
   - AOI polygon selector.
   - Input layer selector.
   - Output CRS selector.
   - Raster bands input row.
   - Output mode selector.
   - Output file row.
   - Layer details panel and OK/Cancel buttons.
4. Implement dialog behavior in processing_demo_dialog.py with:
   - AOI polygon selector.
   - Input layer selector.
   - Output CRS selector.
   - Raster bands input (shown only for raster).
   - Output mode selector: Temporary layer or Save to file.
   - Output file picker (enabled only in Save to file mode).
5. Populate layer selectors from current QGIS project layers.
6. Enforce that AOI and input layer are separate selections.
7. Add layer details panel:
   - Vector: geometry type, feature count, CRS.
   - Raster: band count, raster size, CRS.
8. Validate dialog inputs before running:
   - AOI is selected.
   - Input layer is selected.
   - Output path is set when Save to file is selected.
   - Raster bands are valid indices for the selected raster.
9. In processing_demo.py execute workflow by layer type:
   - Vector branch:
     - native:clip
     - native:reprojectlayer
   - Raster branch:
     - gdal:cliprasterbymasklayer
     - gdal:warpreproject
     - gdal:translate with selected bands as final step
10. Add resulting output layer to the map when valid.
11. Log status and errors to the QGIS message bar and message log.

## Plugin Reloader Workflow

1. Install Plugin Reloader from QGIS Plugins manager.
2. Enable processing_demo plugin once.
3. After each code change:
   - Use Plugin Reloader to reload processing_demo.
   - Reopen the plugin dialog and continue iterating.

## Package as ZIP

When you want to share the plugin with another machine or workshop attendee, build a ZIP package from the plugin folder:

```bash
cd processing_demo
pb_tool zip
```

This creates `processing_demo.zip` in the plugin directory.

## Install from ZIP in QGIS

1. Open QGIS.
2. Go to Plugins > Manage and Install Plugins.
3. Open the Install from ZIP tab.
4. Browse to the `processing_demo.zip` file.
5. Click Install Plugin.
6. Enable the plugin if needed.

## Symlink Setup for Seamless Loading

Link ./processing_demo into your QGIS profile plugins directory so edits are picked up immediately.

Windows (PowerShell as Administrator):

```powershell
New-Item -ItemType SymbolicLink `
   -Path "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\processing_demo" `
   -Target "C:\path\to\qgis\processing_demo"
```

Linux:

```bash
ln -s /path/to/qgis/processing_demo ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/processing_demo
```

macOS:

```bash
ln -s /path/to/qgis/processing_demo "$HOME/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/processing_demo"
```

Tip: If a plugins/processing_demo folder already exists in the QGIS profile, remove it first before creating the symlink.

## uv Dependency Management

Use uv to keep workshop dependencies simple and reproducible.

1. Create project metadata in ./processing_demo if missing.
   - Add pyproject.toml with minimal project information.
2. Create virtual environment and install tooling.

```bash
cd processing_demo
uv init
uv add --dev pb-tool ruff
```

1. Use uv-run style commands when needed.

```bash
uv run pb_tool --help
```

## Workshop Notes

- Keep the UI intentionally minimal and readable.
- Focus on understanding AOI clipping, layer types, CRS transformation, and output choices.
- Avoid advanced options not required for beginner fundamentals.
