import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from facade import ImageAnalyzerFacade


class PaletteGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Paletas de Colores")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.facade = ImageAnalyzerFacade()
        self.image_path = None
        self.palette = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🎨 Generador de Paletas de Colores",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para selección de imagen
        select_frame = tk.Frame(main_frame, bg="#f0f0f0")
        select_frame.pack(fill=tk.X, pady=10)
        
        self.select_btn = tk.Button(
            select_frame,
            text="📁 Seleccionar Imagen",
            command=self.select_image,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        self.image_label = tk.Label(
            select_frame,
            text="Ninguna imagen seleccionada",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        self.image_label.pack(side=tk.LEFT, padx=10)
        
        # Frame para controles
        controls_frame = tk.Frame(main_frame, bg="#f0f0f0")
        controls_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            controls_frame,
            text="Número de colores:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=5)
        
        self.clusters_var = tk.IntVar(value=5)
        self.clusters_spinbox = tk.Spinbox(
            controls_frame,
            from_=2,
            to=10,
            textvariable=self.clusters_var,
            width=5,
            font=("Arial", 11)
        )
        self.clusters_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.generate_btn = tk.Button(
            controls_frame,
            text="✨ Generar Paleta",
            command=self.generate_palette,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.generate_btn.pack(side=tk.LEFT, padx=20)
        
        # Frame para preview de imagen
        preview_frame = tk.LabelFrame(
            main_frame,
            text="Vista Previa de la Imagen",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = tk.Label(
            preview_frame,
            text="La imagen seleccionada aparecerá aquí",
            bg="white",
            fg="#999",
            font=("Arial", 10)
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Frame para paleta de colores
        palette_frame = tk.LabelFrame(
            main_frame,
            text="Paleta de Colores Generada",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        palette_frame.pack(fill=tk.X, pady=10)
        
        self.palette_canvas = tk.Canvas(
            palette_frame,
            height=120,
            bg="white",
            highlightthickness=0
        )
        self.palette_canvas.pack(fill=tk.X, pady=5)
        
        # Frame para botones de exportación
        export_frame = tk.Frame(main_frame, bg="#f0f0f0")
        export_frame.pack(fill=tk.X, pady=10)
        
        self.export_json_btn = tk.Button(
            export_frame,
            text="💾 Exportar JSON",
            command=lambda: self.export_palette("json"),
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.export_json_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_png_btn = tk.Button(
            export_frame,
            text="🖼️ Exportar PNG",
            command=lambda: self.export_palette("png"),
            font=("Arial", 10),
            bg="#9C27B0",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.export_png_btn.pack(side=tk.LEFT, padx=5)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.image_label.config(text=f"Imagen: {filename}")
            self.generate_btn.config(state=tk.NORMAL)
            self.show_image_preview()
    
    def show_image_preview(self):
        try:
            img = Image.open(self.image_path)
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
    
    def generate_palette(self):
        if not self.image_path:
            messagebox.showwarning("Advertencia", "Por favor selecciona una imagen primero")
            return
        
        try:
            self.generate_btn.config(state=tk.DISABLED, text="Generando...")
            self.root.update()
            
            n_clusters = self.clusters_var.get()
            self.palette = self.facade.analyze(
                self.image_path,
                method="kmeans",
                n_clusters=n_clusters
            )
            
            self.display_palette()
            self.generate_btn.config(state=tk.NORMAL, text="✨ Generar Paleta")
            self.export_json_btn.config(state=tk.NORMAL)
            self.export_png_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo("Éxito", "¡Paleta generada correctamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar paleta: {str(e)}")
            self.generate_btn.config(state=tk.NORMAL, text="✨ Generar Paleta")
    
    def display_palette(self):
        self.palette_canvas.delete("all")
        
        if not self.palette:
            return
        
        canvas_width = self.palette_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 800
        
        num_colors = len(self.palette.clusters)
        color_width = canvas_width / num_colors
        
        for i, cluster in enumerate(self.palette.clusters):
            r, g, b = cluster.rgb
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            x1 = i * color_width
            x2 = (i + 1) * color_width
            
            # Rectángulo de color
            self.palette_canvas.create_rectangle(
                x1, 0, x2, 80,
                fill=hex_color,
                outline=""
            )
            
            # Texto con valor hexadecimal
            text_color = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"
            
            self.palette_canvas.create_text(
                (x1 + x2) / 2, 40,
                text=hex_color.upper(),
                fill=text_color,
                font=("Arial", 10, "bold")
            )
            
            # Valores RGB
            self.palette_canvas.create_text(
                (x1 + x2) / 2, 95,
                text=f"RGB({r}, {g}, {b})",
                font=("Arial", 8),
                fill="#333"
            )
    
    def export_palette(self, fmt):
        if not self.palette:
            messagebox.showwarning("Advertencia", "Genera una paleta primero")
            return
        
        ext = "json" if fmt == "json" else "png"
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{ext}",
            filetypes=[(f"Archivo {ext.upper()}", f"*.{ext}")]
        )
        
        if file_path:
            try:
                self.facade.export(self.palette, fmt, file_path)
                messagebox.showinfo("Éxito", f"Paleta exportada a: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")


def main():
    root = tk.Tk()
    app = PaletteGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()