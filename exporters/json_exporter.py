import json

class JSONExporter:
    def export(self, palette, output_path):
        data = {
            "palette": [cluster.rgb for cluster in palette]
        }
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
