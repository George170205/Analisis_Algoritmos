# factory.py
from analyzers.kmeans_analyzer import KMeansAnalyzer  # Sin punto

class AnalyzerFactory:
    def create(self, method, **params):
        if method == "kmeans":
            n = params.get("n_clusters", 5)
            return KMeansAnalyzer(n_clusters=n)
        else:
            raise ValueError("Método desconocido: " + method)