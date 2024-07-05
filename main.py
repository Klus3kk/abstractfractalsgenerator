import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
import threading

# Center the window on the screen
def center_window(window, width=1000, height=800):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to draw different types of fractals
def draw_fractal(fractal_type, order=0, zoom_factor=1.0, max_iter=256, cmap='nipy_spectral'):
    def mandelbrot(ax, xlim, ylim):
        x = np.linspace(xlim[0], xlim[1], 800)
        y = np.linspace(ylim[0], ylim[1], 800)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        img = np.zeros(C.shape, dtype=int)
        for n in range(max_iter):
            mask = np.abs(Z) < 10
            Z[mask] = Z[mask] * Z[mask] + C[mask]
            img[mask & (np.abs(Z) >= 10)] = n
        ax.imshow(img, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), cmap=cmap)

    def multibrot(ax, xlim, ylim):
        x = np.linspace(xlim[0], xlim[1], 800)
        y = np.linspace(ylim[0], ylim[1], 800)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        img = np.zeros(C.shape, dtype=int)
        for n in range(max_iter):
            mask = np.abs(Z) < 10
            Z[mask] = Z[mask] ** order + C[mask]
            img[mask & (np.abs(Z) >= 10)] = n
        ax.imshow(img, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), cmap=cmap)

    def nova(ax, xlim, ylim):
        x = np.linspace(xlim[0], xlim[1], 800)
        y = np.linspace(ylim[0], ylim[1], 800)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        for n in range(max_iter):
            Z = Z - (Z**3 - 1) / (3 * Z**2)
            Z[abs(Z) > 2] = 0
        ax.imshow(np.angle(Z), extent=(xlim[0], xlim[1], ylim[0], ylim[1]), cmap=cmap)

    def phoenix(ax, xlim, ylim):
        x = np.linspace(xlim[0], xlim[1], 800)
        y = np.linspace(ylim[0], xlim[1], 800)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        P = np.zeros_like(Z)
        for n in range(max_iter):
            Z, P = Z**2 + 0.56667 - 0.5j + P * 0.5, Z
        ax.imshow(np.angle(Z), extent=(xlim[0], xlim[1], ylim[0], ylim[1]), cmap=cmap)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    xlim = [-2.0 / zoom_factor, 2.0 / zoom_factor]
    ylim = [-2.0 / zoom_factor, 2.0 / zoom_factor]

    if fractal_type == "Mandelbrot":
        mandelbrot(ax, xlim=xlim, ylim=ylim)
    elif fractal_type == "Multibrot":
        multibrot(ax, xlim=xlim, ylim=ylim)
    elif fractal_type == "Nova":
        nova(ax, xlim=xlim, ylim=ylim)
    elif fractal_type == "Phoenix":
        phoenix(ax, xlim=xlim, ylim=ylim)

    # Save the fractal as a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close(fig)

    return buf

# Function to generate frames for the video
def generate_frames(fractal_type, order, duration, zoom_speed=1.01):
    frames = []
    zoom_factor = 1.0
    for _ in range(60 * duration):  # 60 frames per second * duration
        buf = draw_fractal(fractal_type, order, zoom_factor)
        img = Image.open(buf)
        frames.append(img)
        zoom_factor *= zoom_speed
    return frames

# Function to play the generated frames
def play_frames(frames, panel):
    def update_frame(frame_idx):
        if frame_idx < len(frames):
            img = frames[frame_idx]
            img_tk = ImageTk.PhotoImage(img)
            panel.config(image=img_tk)
            panel.image = img_tk
            root.after(17, lambda: update_frame(frame_idx + 1))  # 17 ms for ~60 fps

    update_frame(0)

# Function to start generating and playing fractal video
def start_fractal_video():
    fractal_type = fractal_type_var.get()
    order = order_var.get()
    duration = duration_var.get()
    try:
        # Run frame generation in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=lambda: play_frames(generate_frames(fractal_type, order, duration), panel))
        thread.start()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to save the fractal as an image
def save_image():
    fractal_type = fractal_type_var.get()
    order = order_var.get()
    try:
        buf = draw_fractal(fractal_type, order)
        img = Image.open(buf)
        filename = simpledialog.askstring("Save As", "Enter the file name to save (e.g., fractal.png):")
        if filename:
            img.save(filename)
            messagebox.showinfo("Saved", f"Fractal saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to save the fractal as a GIF
def save_gif():
    fractal_type = fractal_type_var.get()
    max_order = order_var.get()
    duration = duration_var.get()
    try:
        frames = generate_frames(fractal_type, max_order, duration)
        filename = simpledialog.askstring("Save As", "Enter the file name to save (e.g., fractal.gif):")
        if filename:
            frames[0].save(filename, save_all=True, append_images=frames[1:], duration=17, loop=0)
            messagebox.showinfo("Saved", f"Fractal GIF saved as {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup the main window
root = tk.Tk()
root.title("Fractal Drawer")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create canvas for fractal display
canvas = tk.Canvas(main_frame, width=800, height=800, bg='black')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create frame for controls
control_frame = tk.Frame(main_frame)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Fractal type selection
fractal_type_var = tk.StringVar(value="Mandelbrot")
ttk.Label(control_frame, text="Fractal Type:").pack()
fractal_type_menu = ttk.Combobox(control_frame, textvariable=fractal_type_var, values=["Mandelbrot", "Multibrot", "Nova", "Phoenix"])
fractal_type_menu.pack()

# Order selection
order_var = tk.IntVar(value=0)
ttk.Label(control_frame, text="Order (for Multibrot):").pack()
order_scale = ttk.Scale(control_frame, from_=0, to=10, variable=order_var, orient=tk.HORIZONTAL)
order_scale.pack()

# GIF duration selection
duration_var = tk.IntVar(value=1)
ttk.Label(control_frame, text="GIF Duration (seconds):").pack()
duration_scale = ttk.Scale(control_frame, from_=1, to=10, variable=duration_var, orient=tk.HORIZONTAL)
duration_scale.pack()

# Buttons
draw_button = ttk.Button(control_frame, text="Draw Fractal", command=start_fractal_video)
draw_button.pack()

save_button = ttk.Button(control_frame, text="Save Fractal", command=save_image)
save_button.pack()

save_gif_button = ttk.Button(control_frame, text="Save Fractal as GIF", command=save_gif)
save_gif_button.pack()

# Panel to display fractal
panel = ttk.Label(canvas)
panel.pack()

# Center the window
center_window(root)

# Start the main loop
root.mainloop()
