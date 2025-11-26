from PIL import Image

class PNGExporter:
    def export(self, palette, output_path):
        width = 50 * len(palette.clusters)
        img = Image.new("RGB", (width, 50))

        for i, cluster in enumerate(palette.clusters):
            color = cluster.rgb
            for x in range(i * 50, (i + 1) * 50):
                for y in range(50):
                    img.putpixel((x, y), color)

        img.save(output_path)
