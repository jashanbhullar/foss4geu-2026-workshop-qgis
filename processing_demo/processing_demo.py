import os.path

from qgis import processing
from qgis.core import (
    Qgis,
    QgsMapLayer,
    QgsMapLayerType,
    QgsMessageLog,
    QgsProject,
    QgsRasterLayer,
    QgsSettings,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .processing_demo_dialog import processing_demoDialog


class processing_demo:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QgsSettings().value("locale/userLocale", QLocale().name())[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", "{}.qm".format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&processing_demo")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("processing_demo", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.add_action(
            icon_path,
            text=self.tr("processing_demo"),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr("&processing_demo"), action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = processing_demoDialog()

        # show the dialog
        self.dlg.refresh_layers()
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            try:
                config = self.dlg.get_config()
                self._run_workflow(config)
                self._log("Processing completed.", Qgis.Success)
            except Exception as exc:
                self._log(f"Processing failed: {exc}", Qgis.Critical)

    def _run_workflow(self, config):
        aoi_layer = config["aoi_layer"]
        input_layer = config["input_layer"]
        target_crs = config["target_crs"]
        output_destination = config["output_destination"]

        if input_layer.type() == QgsMapLayerType.VectorLayer:
            output = self._run_vector_workflow(
                aoi_layer,
                input_layer,
                target_crs,
                output_destination,
            )
            self._add_output_layer(
                output, input_layer.name() + "_processed", is_raster=False
            )
            return

        if input_layer.type() == QgsMapLayerType.RasterLayer:
            output = self._run_raster_workflow(
                aoi_layer,
                input_layer,
                target_crs,
                config["raster_bands"],
                output_destination,
            )
            self._add_output_layer(
                output, input_layer.name() + "_processed", is_raster=True
            )
            return

        raise ValueError("Unsupported input layer type. Use a vector or raster layer.")

    def _run_vector_workflow(
        self, aoi_layer, vector_layer, target_crs, output_destination
    ):
        self._log("Running vector branch: clip then final reprojection.")
        clipped = processing.run(
            "native:clip",
            {
                "INPUT": vector_layer,
                "OVERLAY": aoi_layer,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        reprojected = processing.run(
            "native:reprojectlayer",
            {
                "INPUT": clipped["OUTPUT"],
                "TARGET_CRS": target_crs,
                "OUTPUT": output_destination,
            },
        )
        return reprojected["OUTPUT"]

    def _run_raster_workflow(
        self,
        aoi_layer,
        raster_layer,
        target_crs,
        selected_bands,
        output_destination,
    ):
        self._log("Running raster branch: clip, warp, then final band selection.")

        clipped = processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": raster_layer,
                "MASK": aoi_layer,
                "CROP_TO_CUTLINE": True,
                "KEEP_RESOLUTION": True,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        warped = processing.run(
            "gdal:warpreproject",
            {
                "INPUT": clipped["OUTPUT"],
                "TARGET_CRS": target_crs,
                "RESAMPLING": 1,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        band_args = []
        for band in selected_bands:
            band_args.extend(["-b", str(band)])

        translated = processing.run(
            "gdal:translate",
            {
                "INPUT": warped["OUTPUT"],
                "EXTRA": " ".join(band_args),
                "OUTPUT": output_destination,
            },
        )
        return translated["OUTPUT"]

    def _add_output_layer(self, output, layer_name, is_raster):
        if isinstance(output, QgsMapLayer):
            QgsProject.instance().addMapLayer(output)
            return

        if output == "TEMPORARY_OUTPUT":
            return

        layer = (
            QgsRasterLayer(output, layer_name)
            if is_raster
            else QgsVectorLayer(output, layer_name, "ogr")
        )

        if layer and layer.isValid():
            QgsProject.instance().addMapLayer(layer)
        else:
            self._log(f"Could not load output layer from: {output}", Qgis.Warning)

    def _log(self, message, level=Qgis.Info):
        QgsMessageLog.logMessage(message, "processing_demo", level)
        self.iface.messageBar().pushMessage(
            "processing_demo", message, level=level, duration=4
        )
