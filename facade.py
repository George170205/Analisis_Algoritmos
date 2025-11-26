# facade.py
from factory import AnalyzerFactory  # Sin punto
from exporters.json_exporter import JSONExporter
from exporters.png_exporter import PNGExporter

class ImageAnalyzerFacade:
    def __init__(self):
        self.factory = AnalyzerFactory()

    def analyze(self, image_path, method="kmeans", **params):
        analyzer = self.factory.create(method, **params)
        palette = analyzer.analyze(image_path)
        return palette

    def export(self, palette, fmt, output_path):
        if fmt == "json":
            JSONExporter().export(palette, output_path)
        elif fmt == "png":
            PNGExporter().export(palette, output_path)
        else:
            raise ValueError("Formato no soportado: " + fmt)