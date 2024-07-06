import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
import sympy as sp

class FractalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Generator")

        # Configure style for modern black UI
        style = ttk.Style(theme="darkly")

        self.fractal_type = tk.StringVar(value="Mandelbrot")
        self.max_iter = tk.IntVar(value=256)
        self.xmin = tk.DoubleVar(value=-2.0)
        self.xmax = tk.DoubleVar(value=1.0)
        self.ymin = tk.DoubleVar(value=-1.5)
        self.ymax = tk.DoubleVar(value=1.5)
        self.width = tk.IntVar(value=800)
        self.height = tk.IntVar(value=600)
        self.colormap = tk.StringVar(value="Blues")

        self.custom_eq = tk.StringVar(value="z**2 + c")
        self.custom_c_real = tk.DoubleVar(value=-0.7)
        self.custom_c_imag = tk.DoubleVar(value=0.27015)
        self.custom_z_real = tk.DoubleVar(value=0)
        self.custom_z_imag = tk.DoubleVar(value=0)

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(control_frame, text="Fractal Type").pack(pady=5)
        fractal_combobox = ttk.Combobox(control_frame, textvariable=self.fractal_type, values=[
            "Mandelbrot", "Julia", "Burning Ship", "Tricorn", "Newton",
            "Multibrot", "Mandelbar", "Perpendicular Mandelbrot",
            "Perpendicular Burning Ship", "Perpendicular Buffalo",
            "Celtic Mandelbrot", "Celtic Mandelbar"
        ])
        fractal_combobox.pack(pady=5)
        fractal_combobox.bind("<<ComboboxSelected>>")

        ttk.Label(control_frame, text="Max Iterations").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.max_iter).pack(pady=5)

        ttk.Label(control_frame, text="X Min").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.xmin).pack(pady=5)

        ttk.Label(control_frame, text="X Max").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.xmax).pack(pady=5)

        ttk.Label(control_frame, text="Y Min").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.ymin).pack(pady=5)

        ttk.Label(control_frame, text="Y Max").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.ymax).pack(pady=5)

        ttk.Label(control_frame, text="Width").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.width).pack(pady=5)

        ttk.Label(control_frame, text="Height").pack(pady=5)
        ttk.Entry(control_frame, textvariable=self.height).pack(pady=5)

        ttk.Label(control_frame, text="Colormap").pack(pady=5)
        ttk.Combobox(control_frame, textvariable=self.colormap, values=plt.colormaps()).pack(pady=5)

        ttk.Button(control_frame, text="Generate", command=self.update_plot).pack(pady=10)
        ttk.Button(control_frame, text="Save", command=self.save_plot).pack(pady=5)

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.update_plot()

    def reset_parameters(self, event=None):
        self.max_iter.set(256)
        self.xmin.set(-2.0)
        self.xmax.set(1.0)
        self.ymin.set(-1.5)
        self.ymax.set(1.5)
        self.width.set(800)
        self.height.set(600)

    def mandelbrot(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def julia(self, z, c, max_iter):
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def burning_ship(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), abs(z.imag))
            z = z*z + c
        return max_iter

    def tricorn(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = np.conj(z)*np.conj(z) + c
        return max_iter

    def newton(self, z, max_iter):
        for n in range(max_iter):
            if abs(z**3 - 1) < 1e-6:
                return n
            z = z - (z**3 - 1)/(3*z**2)
        return max_iter

    def multibrot(self, c, max_iter, power=3):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z**power + c
        return max_iter

    def mandelbar(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = np.conj(z*z) + c
        return max_iter

    def perpendicular_mandelbrot(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = np.conj(z*z) + c
        return max_iter

    def perpendicular_burning_ship(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), abs(z.imag))
            z = np.conj(z*z) + c
        return max_iter

    def perpendicular_buffalo(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), -abs(z.imag))
            z = z*z + c
        return max_iter

    def celtic_mandelbrot(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), z.imag)
            z = z*z + c
        return max_iter

    def celtic_mandelbar(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = np.conj(complex(abs(z.real), z.imag)) + c
        return max_iter

    def generate_fractal(self, xmin, xmax, ymin, ymax, width, height, max_iter, fractal_type):
        r1 = np.linspace(xmin, xmax, width)
        r2 = np.linspace(ymin, ymax, height)
        n3 = np.empty((width, height))
        if fractal_type == "Mandelbrot":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.mandelbrot(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Julia":
            c = complex(self.custom_c_real.get(), self.custom_c_imag.get())
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.julia(r1[i] + 1j*r2[j], c, max_iter)
        elif fractal_type == "Burning Ship":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.burning_ship(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Tricorn":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.tricorn(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Newton":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.newton(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Multibrot":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.multibrot(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Mandelbar":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.mandelbar(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Perpendicular Mandelbrot":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.perpendicular_mandelbrot(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Perpendicular Burning Ship":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.perpendicular_burning_ship(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Perpendicular Buffalo":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.perpendicular_buffalo(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Celtic Mandelbrot":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.celtic_mandelbrot(r1[i] + 1j*r2[j], max_iter)
        elif fractal_type == "Celtic Mandelbar":
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.celtic_mandelbar(r1[i] + 1j*r2[j], max_iter)
                    
        return n3

    def update_plot(self):
        xmin, xmax = self.xmin.get(), self.xmax.get()
        ymin, ymax = self.ymin.get(), self.ymax.get()
        width, height = self.width.get(), self.height.get()
        max_iter = self.max_iter.get()
        fractal_type = self.fractal_type.get()
        colormap = self.colormap.get()

        z = self.generate_fractal(xmin, xmax, ymin, ymax, width, height, max_iter, fractal_type)
        self.ax.clear()
        self.ax.imshow(z.T, origin='lower', cmap=colormap, extent=[xmin, xmax, ymin, ymax])
        self.canvas.draw()

    def save_plot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            original_xlim = self.ax.get_xlim()
            original_ylim = self.ax.get_ylim()
            original_title = self.ax.get_title()

            self.ax.set_title("")
            self.ax.axis('off')

            self.fig.savefig(file_path, bbox_inches='tight', pad_inches=0)

            self.ax.set_title(original_title)
            self.ax.axis('on')
            self.ax.set_xlim(original_xlim)
            self.ax.set_ylim(original_ylim)

            self.canvas.draw()

    def on_click(self, event):
        if event.dblclick:
            x, y = event.xdata, event.ydata
            span_x = 0.5 * (self.xmax.get() - self.xmin.get())
            span_y = 0.5 * (self.ymax.get() - self.ymin.get())
            self.xmin.set(x - span_x / 4)
            self.xmax.set(x + span_x / 4)
            self.ymin.set(y - span_y / 4)
            self.ymax.set(y + span_y / 4)
            self.update_plot()

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = FractalApp(root)
    root.mainloop()