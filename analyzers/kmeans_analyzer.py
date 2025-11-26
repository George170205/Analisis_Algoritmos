#analyzers/kmeans_analyzers.py
import numpy as np
from sklearn.cluster import KMeans
from .base_analyzers import BaseAnalyzer



class KMeansAnalyzer(BaseAnalyzer):
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters


    def extract_colors(self):
        img = np.array(self.image)
        pixels = img.reshape((-1, 3))


        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(pixels)


        centers = kmeans.cluster_centers_.astype(int)
        return centers