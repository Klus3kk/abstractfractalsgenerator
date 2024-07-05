import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk

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
        self.colormap = tk.StringVar(value="hot")
        
        # Custom fractal parameters
        self.custom_params = {}

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(control_frame, text="Fractal Type").pack(pady=5)
        self.fractal_types = ["Mandelbrot", "Julia", "Burning Ship", "Tricorn", "Newton", "Custom"]
        ttk.Combobox(control_frame, textvariable=self.fractal_type, values=self.fractal_types).pack(pady=5)

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
        
        # Custom fractal parameter inputs
        self.custom_param_entries = []
        self.custom_param_frame = ttk.Frame(control_frame)
        self.custom_param_frame.pack(pady=10)
        ttk.Button(control_frame, text="Add Parameter", command=self.add_custom_param).pack(pady=5)

    def add_custom_param(self):
        param_name = tk.StringVar()
        param_value = tk.DoubleVar()
        frame = ttk.Frame(self.custom_param_frame)
        frame.pack(pady=5)
        ttk.Entry(frame, textvariable=param_name, width=10).pack(side=tk.LEFT)
        ttk.Entry(frame, textvariable=param_value, width=10).pack(side=tk.LEFT)
        self.custom_param_entries.append((param_name, param_value))

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.update_plot()

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
            z = complex(abs(z.real), abs(z.imag))**2 + c
        return max_iter

    def tricorn(self, c, max_iter):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(z.real, -z.imag)**2 + c
        return max_iter

    def newton(self, z, max_iter):
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            try:
                z -= (z**3 - 1) / (3 * z**2)
            except ZeroDivisionError:
                return max_iter
        return max_iter

    def custom_fractal(self, z, c, max_iter, custom_func):
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = custom_func(z, c)
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
            c = complex(-0.7, 0.27015)
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
        elif fractal_type == "Custom":
            custom_func = self.get_custom_function()
            for i in range(width):
                for j in range(height):
                    n3[i, j] = self.custom_fractal(r1[i] + 1j*r2[j], 0, max_iter, custom_func)
        return n3

    def get_custom_function(self):
        def custom_func(z, c):
            for name, value in self.custom_param_entries:
                if name.get() == "z":
                    z = complex(value.get(), value.get())
                elif name.get() == "c":
                    c = complex(value.get(), value.get())
                z = z * c + z
            return z
        return custom_func

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
