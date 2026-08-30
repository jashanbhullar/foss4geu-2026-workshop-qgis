from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
)
from qgis.PyQt.QtCore import QCoreApplication


class CheckNameField(QgsProcessingAlgorithm):
    INPUT = "INPUT"

    def tr(self, text):
        return QCoreApplication.translate("Processing", text)

    def createInstance(self):
        return CheckNameField()

    def name(self):
        return "check_name_field"

    def displayName(self):
        return self.tr(
            'Checking if script reloads if "non-existent-field" field exists'
        )

    def group(self):
        return self.tr("Custom scripts")

    def groupId(self):
        return "customscripts"

    def shortHelpString(self):
        return self.tr(
            'Checks whether the input vector layer contains a field named "name".'
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input vector layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        field_names = [field.name() for field in source.fields()]

        if "non_existent_field" not in field_names:
            raise QgsProcessingException(
                self.tr(
                    'Input layer does not contain a field named "non_existent_field".'
                )
            )

        feedback.pushInfo(
            self.tr('Field "non_existent_field" exists in the input layer.')
        )
        return {}
