#examples/run_example.py
from ..facade import ImageAnalyzerFacade
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True)
parser.add_argument("--clusters", type=int, default=5)
parser.add_argument("--export", choices=["json", "png"], default="json")
parser.add_argument("--out", required=True)
args = parser.parse_args()


facade = ImageAnalyzerFacade()
palette = facade.analyze(args.image, method="kmeans", n_clusters=args.clusters)


print("Paleta generada:", palette)
facade.export(palette, args.export, args.out)
print("Exportado a", args.out)