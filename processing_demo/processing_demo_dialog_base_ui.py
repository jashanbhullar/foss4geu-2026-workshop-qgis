"""UI scaffold for the workshop plugin dialog.

This module defines a hand-written Qt widget tree instead of relying on a
generated .ui conversion step. The goal is to keep the workshop code easy to
read and easy to modify in plain Python.

The dialog is organized into three main sections:
1. A short instruction banner.
2. An Inputs group with AOI, input layer, CRS, bands, and output controls.
3. A Layer Details panel plus standard OK/Cancel actions.

The logic and signal wiring are implemented in processing_demo_dialog.py.
This module is intentionally limited to visual structure and widget creation.
"""

from qgis.gui import QgsProjectionSelectionWidget
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_processing_demoDialogBase:
    """Base UI for the workshop dialog.

    This file is kept intentionally simple so participants can read and modify it
    without using Qt Designer.
    """

    def setupUi(self, dialog):
                """Build the full widget hierarchy for the plugin dialog.

                Parameters
                ----------
                dialog : QDialog
                        Parent dialog instance that receives all widgets and layouts.

                Notes
                -----
                - The raster band controls are always created but may be hidden later
                    by dialog logic depending on selected input layer type.
                - Output controls support either temporary output or file output.
                - This method should only construct UI. Validation and behavior belong
                    in processing_demo_dialog.py.
                """
        dialog.setWindowTitle("processing_demo")
        dialog.resize(680, 520)

        self.main_layout = QVBoxLayout(dialog)

        self.info_label = QLabel(
            "Choose AOI and an input layer. The plugin clips first, then reprojects."
        )
        self.info_label.setWordWrap(True)
        self.main_layout.addWidget(self.info_label)

        self.inputs_group = QGroupBox("Inputs")
        self.inputs_layout = QFormLayout(self.inputs_group)

        self.aoi_combo = QComboBox()
        self.inputs_layout.addRow("AOI (polygon):", self.aoi_combo)

        self.input_layer_combo = QComboBox()
        self.inputs_layout.addRow("Input layer:", self.input_layer_combo)

        self.target_crs_widget = QgsProjectionSelectionWidget()
        self.inputs_layout.addRow("Output CRS:", self.target_crs_widget)

        self.raster_bands_row = QWidget()
        self.raster_bands_layout = QHBoxLayout(self.raster_bands_row)
        self.raster_bands_layout.setContentsMargins(0, 0, 0, 0)
        self.raster_bands_edit = QLineEdit("1,2,3")
        self.raster_bands_edit.setPlaceholderText("Example: 1,2,3")
        self.raster_bands_layout.addWidget(self.raster_bands_edit)
        self.inputs_layout.addRow("Raster bands:", self.raster_bands_row)

        self.output_mode_combo = QComboBox()
        self.output_mode_combo.addItems(["Temporary layer", "Save to file"])
        self.inputs_layout.addRow("Output mode:", self.output_mode_combo)

        self.output_path_row = QWidget()
        self.output_path_layout = QHBoxLayout(self.output_path_row)
        self.output_path_layout.setContentsMargins(0, 0, 0, 0)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("Set path when using Save to file")
        self.output_browse_btn = QPushButton("Browse")
        self.output_path_layout.addWidget(self.output_path_edit)
        self.output_path_layout.addWidget(self.output_browse_btn)
        self.inputs_layout.addRow("Output file:", self.output_path_row)

        self.main_layout.addWidget(self.inputs_group)

        self.details_group = QGroupBox("Layer Details")
        self.details_layout = QVBoxLayout(self.details_group)
        self.layer_details_text = QTextEdit()
        self.layer_details_text.setReadOnly(True)
        self.layer_details_text.setMinimumHeight(160)
        self.details_layout.addWidget(self.layer_details_text)
        self.main_layout.addWidget(self.details_group)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.main_layout.addWidget(self.button_box)
