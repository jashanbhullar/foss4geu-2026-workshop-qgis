# Workshop Plan: QGIS Model Designer and Plugin Development

## Workshop Goal

Demo data package:

- Download the workshop sample data from <https://drive.google.com/file/d/1WvRVhR0BgKlhZuF5ebjVwKEUphy8UP8u/view?usp=sharing>
- Use it for both the Model Designer and plugin demos so attendees follow the same layers throughout the workshop.

Help attendees understand two practical ways to automate GIS workflows in QGIS:

- QGIS Model Designer for quick, shareable workflow automation.
- QGIS Plugin Development for custom, reusable application behavior.

By the end of the workshop, participants should know when to use each approach, what they have in common, and how to start building both.

## Audience

- QGIS users who want to automate repetitive tasks.
- GIS analysts who have custom Python scripts and want to share them.
- Developers who want a practical introduction to QGIS extension points.

## Core Demo Material

This workshop is grounded in three companion documents and the matching demo assets:

- [QGIS-Manual.md](QGIS-Manual.md)
- [QGIS-Model.md](QGIS-Model.md)
- [QGIS-Plugin.md](QGIS-Plugin.md)

The plugin demo now uses the `processing_demo/` workspace and demonstrates:

- AOI selection.
- Output CRS selection.
- Vector or raster layer selection.
- Dynamic layer details.
- Raster band selection when needed.
- Temporary output or saved output.

The manual and model docs demonstrate the same workflow pattern:

- Clip first in source CRS.
- Reproject only the final clipped output.
- For raster, select bands as the last step.

The model doc also includes a bonus custom-script step using `validation_demo.py`.

## 2-Hour Agenda

### 0:00 - 0:10 Introduction

- Introduce the problem: repeating manual GIS work is slow and error-prone.
- Explain the workshop structure.
- Set expectations for both paths:
  - Model Designer for orchestration.
  - Plugin Development for custom UI and logic.

### 0:10 - 0:20 Similarities and Differences

- Similarities:
  - Both automate QGIS workflows.
  - Both can be shared with a team.
  - Both can wrap Python-based logic.
- Differences:
  - Model Designer is low-code and good for chaining tools.
  - Plugins are better when you need custom UI, custom validation, and richer packaging.
  - Models are faster to build; plugins are more flexible.

### 0:20 - 0:55 Part 1: QGIS Model Designer First

#### Milestone 1: Build a simple model

- Open Model Designer.
- Add an AOI polygon input.
- Add either a vector or raster input.
- Show clip-first, reproject-last behavior.
- For raster, show band selection at the end.
- Show how model steps can be chained without writing a full plugin.

#### Milestone 2: Save and load the model

- Save the model to disk.
- Reopen it to show portability and reuse.
- Explain how this makes the workflow shareable across a team.

#### Milestone 3: Add a Python step

- Show how the `validation_demo.py` script can be used as one step in the model.
- Explain how the custom script validates vector input before the main workflow.
- Explain when this is enough and when it is not.

#### Milestone 4: Discuss practical constraints

- Limited UI control.
- Good for linear workflows.
- Best when the main requirement is repeatability, not a custom product.

### 0:55 - 1:00 Transition

- Summarize what Model Designer solved well.
- Frame the next section as the path for when a model is not enough.

### 1:00 - 1:40 Part 2: QGIS Plugin Development

#### Milestone 5: Inspect the plugin structure

- Show the plugin scaffold in the `processing_demo/` folder.
- Point out `processing_demo.py`, `processing_demo_dialog.py`, `processing_demo_dialog_base_ui.py`, metadata, and tests.
- Explain how plugin packaging differs from a model file.

#### Milestone 6: Walk through the plugin workflow

- Open the plugin dialog.
- Select an AOI polygon.
- Select an input vector or raster layer.
- Show the layer details panel updating by layer type.
- If raster is selected, show band selection.
- Choose temporary output or save-to-file output.
- Show the clip-first, final-reproject workflow.

#### Milestone 7: Show the custom logic layer

- Discuss the processing functions that handle raster and vector inputs.
- Explain why a plugin is useful when you need:
  - Custom validation.
  - Dedicated UI.
  - Multiple workflow branches.
  - Dependency management.
  - A guided workshop-friendly interface.

#### Milestone 8: Cover development setup

- Explain the basic plugin development loop.
- Show how UI and code work together.
- Mention Plugin Builder 3, Plugin Reloader, and uv for dependencies.
- Show the symlink-based reload loop for seamless local development.

### 1:40 - 1:55 Comparison and Decision Guide

- Use Model Designer when the workflow is mostly a chain of existing tools.
- Use a plugin when users need a guided application-like experience.
- Use both together when the model is the workflow engine and the plugin is the front door.

### 1:55 - 2:00 Wrap-Up

- Recap the decision points.
- Invite questions.
- Point attendees to next steps for their own workflows.

## Milestone Summary

1. Understand where Model Designer fits.
2. Build and save a basic model with AOI, vector/raster branching, and final reprojection.
3. Add a custom validation script step to the model.
4. Understand the plugin scaffold and runtime flow.
5. Run a custom plugin workflow for raster and vector inputs.
6. Compare both approaches and choose the right one for a use case.

## Suggested Demo Outcomes

- A saved model that attendees can reuse immediately.
- A working plugin walkthrough that turns layer input into a clipped, reprojected output.
- A simple mental model for choosing between models and plugins.

## Presenter Notes

- Keep the model section practical and fast so the plugin section still has enough time.
- Use the plugin demo to show why custom UI, validation, and output control matter.
- If time gets tight, shorten the model scripting detail before shortening the plugin walkthrough.
- Keep the bonus custom-script step as an optional stretch goal if the room is moving quickly.

## Sources

### QGIS Documentation

- QGIS Model Designer: <https://docs.qgis.org/latest/en/docs/user_manual/processing/modeler.html>
- QGIS Plugins (PyQGIS Developer Cookbook): <https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/plugins/index.html>

### uv Documentation

- uv official docs: <https://docs.astral.sh/uv/>

### Qt5 Documentation

- Qt 5 documentation index: <https://doc.qt.io/qt-5/>

### Additional Workshop References

- YouTube: <https://www.youtube.com/watch?v=bK9Je14BXbI&pp=ygUTcWdpcyBtb2RlbCBkZXNpZ25lcg%3D%3D>
- YouTube: <https://www.youtube.com/watch?v=axvuyA52yoU&pp=ygUTcWdpcyBtb2RlbCBkZXNpZ25lcg%3D%3D>
- QGIS Tutorials (Python plugin): <https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html>
- <https://spatialthoughts.com/2024/11/29/qgis-coditional-input-model/#more-14383>
