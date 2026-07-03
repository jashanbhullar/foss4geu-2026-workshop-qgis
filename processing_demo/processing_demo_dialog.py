"""Dialog behavior for the workshop processing plugin.

This module implements the interactive logic for selecting:
- an AOI polygon layer,
- an input layer (vector or raster),
- an output CRS,
- optional raster band selection,
- and output destination mode.

The dialog is designed for workshop clarity rather than exhaustive options.
It keeps behavior explicit and validates user choices before processing starts.
"""

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsMapLayerType,
    QgsProject,
    QgsWkbTypes,
)
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox

from .processing_demo_dialog_base_ui import Ui_processing_demoDialogBase


class processing_demoDialog(QDialog, Ui_processing_demoDialogBase):
    """Workshop dialog with AOI/input/output controls and validation.

    Responsibilities
    ----------------
    - Populate combo boxes from current project layers.
    - Keep AOI and input choices distinct.
    - Expose human-readable layer metadata to the user.
    - Validate configuration before accepting the dialog.
    - Provide a normalized config dictionary consumed by plugin workflow code.
    """

    def __init__(self, parent=None):
        """Initialize widgets, defaults, and signal wiring.

        Parameters
        ----------
        parent : QWidget | None
            Optional parent widget passed by QGIS.
        """
        super().__init__(parent)
        self.setupUi(self)

        self._layers_by_id = {}
        self.target_crs_widget.setCrs(QgsCoordinateReferenceSystem("EPSG:8857"))

        self.aoi_combo.currentIndexChanged.connect(self._on_aoi_changed)
        self.input_layer_combo.currentIndexChanged.connect(self._on_input_changed)
        self.output_mode_combo.currentIndexChanged.connect(self._on_output_mode_changed)
        self.output_browse_btn.clicked.connect(self._on_browse_output)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.refresh_layers()
        self._on_output_mode_changed()
        self._on_input_changed()

    def refresh_layers(self):
        """Refresh layer caches and repopulate AOI and input selectors.

        This method reads all layers currently loaded in the active QGIS
        project, sorts them by name for predictable display, and updates
        internal ID-to-layer mapping used by helper accessors.
        """
        all_layers = list(QgsProject.instance().mapLayers().values())
        all_layers.sort(key=lambda lyr: lyr.name().lower())
        self._layers_by_id = {lyr.id(): lyr for lyr in all_layers}

        self.aoi_combo.blockSignals(True)
        self.aoi_combo.clear()
        self.aoi_combo.addItem("Select AOI polygon layer...", "")
        for lyr in all_layers:
            if self._is_polygon_layer(lyr):
                self.aoi_combo.addItem(lyr.name(), lyr.id())
        self.aoi_combo.blockSignals(False)

        self._populate_input_combo()

    def _populate_input_combo(self):
        """Populate input-layer choices, excluding the selected AOI layer."""
        selected_aoi_id = self.aoi_combo.currentData() or ""
        self.input_layer_combo.blockSignals(True)
        self.input_layer_combo.clear()
        self.input_layer_combo.addItem("Select input layer...", "")
        for lyr in self._layers_by_id.values():
            if lyr.id() == selected_aoi_id:
                continue
            self.input_layer_combo.addItem(lyr.name(), lyr.id())
        self.input_layer_combo.blockSignals(False)
        self._on_input_changed()

    def _is_polygon_layer(self, layer):
        """Return True when a layer is a vector polygon layer."""
        if layer.type() != QgsMapLayerType.VectorLayer:
            return False
        return layer.geometryType() == QgsWkbTypes.PolygonGeometry

    def _on_aoi_changed(self):
        """React to AOI changes by rebuilding valid input choices."""
        self._populate_input_combo()

    def _on_input_changed(self):
        """Update UI state and details panel after input-layer changes.

        Behavior
        --------
        - Show raster band controls only for raster input layers.
        - Show a guidance message when no input is selected.
        - Display key metadata relevant to the selected layer type.
        """
        layer = self.selected_input_layer()
        is_raster = bool(layer and layer.type() == QgsMapLayerType.RasterLayer)
        self.raster_bands_row.setVisible(is_raster)

        if not layer:
            self.layer_details_text.setPlainText(
                "Select an input layer to view details."
            )
            return

        details = [f"Name: {layer.name()}", f"CRS: {layer.crs().authid() or 'Unknown'}"]
        if layer.type() == QgsMapLayerType.VectorLayer:
            details.extend(
                [
                    "Type: Vector",
                    f"Geometry: {QgsWkbTypes.displayString(layer.wkbType())}",
                    f"Feature count: {layer.featureCount()}",
                ]
            )
        elif layer.type() == QgsMapLayerType.RasterLayer:
            details.extend(
                [
                    "Type: Raster",
                    f"Band count: {layer.bandCount()}",
                    f"Size: {layer.width()} x {layer.height()}",
                ]
            )

        self.layer_details_text.setPlainText("\n".join(details))

    def _on_output_mode_changed(self):
        """Enable or disable output path controls by output mode."""
        save_to_file = self.output_mode_combo.currentText() == "Save to file"
        self.output_path_edit.setEnabled(save_to_file)
        self.output_browse_btn.setEnabled(save_to_file)

    def _on_browse_output(self):
        """Open file chooser with filter based on selected input type."""
        layer = self.selected_input_layer()
        if layer and layer.type() == QgsMapLayerType.RasterLayer:
            flt = "GeoTIFF (*.tif *.tiff)"
            default_name = "processing_demo_raster.tif"
        else:
            flt = "GeoPackage (*.gpkg);;ESRI Shapefile (*.shp)"
            default_name = "processing_demo_vector.gpkg"

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Select output file", default_name, flt
        )
        if output_path:
            self.output_path_edit.setText(output_path)

    def selected_aoi_layer(self):
        """Return currently selected AOI layer object or None."""
        return self._layers_by_id.get(self.aoi_combo.currentData() or "")

    def selected_input_layer(self):
        """Return currently selected input layer object or None."""
        return self._layers_by_id.get(self.input_layer_combo.currentData() or "")

    def selected_bands(self):
        """Parse raster band text into a list of integer band indices.

        Returns
        -------
        list[int]
            Empty list when no text is provided.

        Raises
        ------
        ValueError
            If any token cannot be parsed as an integer.
        """
        raw = self.raster_bands_edit.text().strip()
        if not raw:
            return []
        bands = []
        for part in raw.split(","):
            value = part.strip()
            if value:
                bands.append(int(value))
        return bands

    def output_destination(self):
        """Return TEMPORARY_OUTPUT marker or selected output file path."""
        if self.output_mode_combo.currentText() == "Temporary layer":
            return "TEMPORARY_OUTPUT"
        return self.output_path_edit.text().strip()

    def get_config(self):
        """Build normalized configuration consumed by processing workflow.

        Returns
        -------
        dict
            Dictionary with selected layers, CRS, raster bands, and output
            destination in a shape expected by processing_demo._run_workflow.
        """
        return {
            "aoi_layer": self.selected_aoi_layer(),
            "input_layer": self.selected_input_layer(),
            "target_crs": self.target_crs_widget.crs(),
            "raster_bands": self.selected_bands(),
            "output_destination": self.output_destination(),
        }

    def _validate(self):
        """Validate user selections before dialog acceptance.

        Checks
        ------
        - AOI and input layer must be selected.
        - Output file path is required in Save to file mode.
        - Raster band values must exist and be in valid index range.

        Raises
        ------
        ValueError
            If any validation rule fails.
        """
        aoi = self.selected_aoi_layer()
        input_layer = self.selected_input_layer()

        if aoi is None:
            raise ValueError("Please select an AOI polygon layer.")

        if input_layer is None:
            raise ValueError("Please select an input layer.")

        if (
            self.output_mode_combo.currentText() == "Save to file"
            and not self.output_path_edit.text().strip()
        ):
            raise ValueError(
                "Please select an output file path or choose Temporary layer."
            )

        if input_layer.type() == QgsMapLayerType.RasterLayer:
            bands = self.selected_bands()
            if not bands:
                raise ValueError("Please provide raster bands, for example 1,2,3.")
            invalid = [b for b in bands if b < 1 or b > input_layer.bandCount()]
            if invalid:
                raise ValueError(
                    f"Band values out of range: {invalid}. Available range is 1..{input_layer.bandCount()}."
                )

    def accept(self):
        """Validate and accept dialog, or show warning message on failure."""
        try:
            self._validate()
        except Exception as exc:
            QMessageBox.warning(self, "Invalid input", str(exc))
            return
        super().accept()
