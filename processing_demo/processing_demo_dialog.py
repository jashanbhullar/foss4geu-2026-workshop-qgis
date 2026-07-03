from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsMapLayerType,
    QgsProject,
    QgsWkbTypes,
)
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox

from .processing_demo_dialog_base_ui import Ui_processing_demoDialogBase


class processing_demoDialog(QDialog, Ui_processing_demoDialogBase):
    """Workshop dialog with minimal AOI/vector/raster controls."""

    def __init__(self, parent=None):
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
        if layer.type() != QgsMapLayerType.VectorLayer:
            return False
        return layer.geometryType() == QgsWkbTypes.PolygonGeometry

    def _on_aoi_changed(self):
        self._populate_input_combo()

    def _on_input_changed(self):
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
        save_to_file = self.output_mode_combo.currentText() == "Save to file"
        self.output_path_edit.setEnabled(save_to_file)
        self.output_browse_btn.setEnabled(save_to_file)

    def _on_browse_output(self):
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
        return self._layers_by_id.get(self.aoi_combo.currentData() or "")

    def selected_input_layer(self):
        return self._layers_by_id.get(self.input_layer_combo.currentData() or "")

    def selected_bands(self):
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
        if self.output_mode_combo.currentText() == "Temporary layer":
            return "TEMPORARY_OUTPUT"
        return self.output_path_edit.text().strip()

    def get_config(self):
        return {
            "aoi_layer": self.selected_aoi_layer(),
            "input_layer": self.selected_input_layer(),
            "target_crs": self.target_crs_widget.crs(),
            "raster_bands": self.selected_bands(),
            "output_destination": self.output_destination(),
        }

    def _validate(self):
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
        try:
            self._validate()
        except Exception as exc:
            QMessageBox.warning(self, "Invalid input", str(exc))
            return
        super().accept()
