# Workshop Plan: QGIS Model Designer and Plugin Development

## Workshop Goal

Help attendees understand two practical ways to automate GIS workflows in QGIS:

- QGIS Model Designer for quick, shareable workflow automation.
- QGIS Plugin Development for custom, reusable application behavior.

By the end of the workshop, participants should know when to use each approach, what they have in common, and how to start building both.

## Audience

- QGIS users who want to automate repetitive tasks.
- GIS analysts who have custom Python scripts and want to share them.
- Developers who want a practical introduction to QGIS extension points.

## Core Demo Material

This workshop is grounded in the example plugin in the `dev/` workspace, which already demonstrates:

- Raster and vector layer handling.
- UI-driven parameter selection.
- Output generation as RGBA GeoTIFF plus legend CSV.
- Packaging results into a ZIP file for sharing.
- Dependency-heavy Python code using libraries such as NumPy, Rasterio, GDAL, and Pillow.

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
- Add a small workflow with a clear input and output.
- Show how model steps can be chained without writing a full plugin.

#### Milestone 2: Save and load the model

- Save the model to disk.
- Reopen it to show portability and reuse.
- Explain how this makes the workflow shareable across a team.

#### Milestone 3: Add a Python step

- Show how a custom Python script can be used as one step in the model.
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

- Show the plugin scaffold in the example plugin folder under `dev/`.
- Point out the main entry file, UI files, metadata, and tests.
- Explain how plugin packaging differs from a model file.

#### Milestone 6: Walk through the plugin workflow

- Open the plugin dialog.
- Select a raster or vector layer.
- Show how the plugin branches based on layer type.
- Explain the output artifacts:
  - RGBA TIFF.
  - Legend CSV.
  - ZIP package for sharing.

#### Milestone 7: Show the custom logic layer

- Discuss the processing functions that handle raster and vector inputs.
- Explain why a plugin is useful when you need:
  - Custom validation.
  - Dedicated UI.
  - Multiple outputs.
  - Dependency management.

#### Milestone 8: Cover development setup

- Explain the basic plugin development loop.
- Show how UI and code work together.
- Mention dependency handling and packaging for teammates.

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
2. Build and save a basic model.
3. Add a Python step to a model.
4. Understand the plugin scaffold and runtime flow.
5. Run a custom plugin workflow for raster and vector inputs.
6. Compare both approaches and choose the right one for a use case.

## Suggested Demo Outcomes

- A saved model that attendees can reuse immediately.
- A working plugin walkthrough that turns layer input into a packaged output.
- A simple mental model for choosing between models and plugins.

## Presenter Notes

- Keep the model section practical and fast so the plugin section still has enough time.
- Use the plugin demo to show why custom UI and packaging matter.
- If time gets tight, shorten the model scripting detail before shortening the plugin walkthrough.
