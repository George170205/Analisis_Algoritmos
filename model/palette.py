#model/palette.py
class ColorCluster:
    def __init__(self, rgb_tuple):
        self.rgb = rgb_tuple # (R, G, B)


    def __repr__(self):
        return f"ColorCluster(rgb={self.rgb})"




class Palette:
    def __init__(self, clusters):
        self.clusters = clusters


    def __iter__(self):
        return iter(self.clusters)


    def __repr__(self):
        return f"Palette({self.clusters})"