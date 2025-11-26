#analyzers/base_analyzers.py
from abc import ABC, abstractmethod
from PIL import Image


class BaseAnalyzer(ABC):
    def analyze(self, image_path):
        self.image = self.load_image(image_path)
        self.preprocess()
        colors = self.extract_colors()
        palette = self.postprocess(colors)
        return palette


    def load_image(self, path):
        return Image.open(path).convert("RGB")


    def preprocess(self):
    # Default: no preprocessing
        pass


    @abstractmethod
    def extract_colors(self):
        pass


    def postprocess(self, colors):
        from ..model.palette import Palette, ColorCluster
        clusters = [ColorCluster(tuple(c)) for c in colors]
        return Palette(clusters)