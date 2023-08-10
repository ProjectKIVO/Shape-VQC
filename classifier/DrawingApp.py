import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class DrawingApp:
    def __init__(self, master):
        self.master = master

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.onclick)
        self.master.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.shape_type = None
        self.points = []
        self.radius = 0

        btn_triangle = tk.Button(master, text="Triangle", command=self.set_triangle)
        btn_triangle.pack(side=tk.LEFT)
        btn_square = tk.Button(master, text="Square", command=self.set_square)
        btn_square.pack(side=tk.LEFT)
        btn_circle = tk.Button(master, text="Circle", command=self.set_circle)
        btn_circle.pack(side=tk.LEFT)
        btn_save = tk.Button(master, text="Save", command=self.on_save)
        btn_save.pack(side=tk.LEFT)

        self.configure_plot()

    def quit_app(self):
        self.master.quit()  # Stop the main loop
        self.master.destroy()  # Destroy the main window

    def set_triangle(self):
        self.shape_type = "Triangle"
        self.clear_plot()
        print("Switched to Triangle mode")

    def set_square(self):
        self.shape_type = "Square"
        self.clear_plot()
        print("Switched to Square mode")

    def set_circle(self):
        self.shape_type = "Circle"
        self.clear_plot()
        print("Switched to Circle mode")

    def on_save(self):
        if self.shape_type:
            label = self.get_label()
            self.save(label)
            self.clear_plot()

    def onclick(self, event):
        x, y = round(event.xdata), round(event.ydata)

        if self.shape_type == "Circle" and len(self.points) == 1:
            self.radius = int(
                ((x - self.points[0][0]) ** 2 + (y - self.points[0][1]) ** 2) ** 0.5
            )
            self.draw_shape()
        else:
            self.points.append((x, y))

            if (self.shape_type == "Triangle" and len(self.points) == 3) or (
                self.shape_type == "Square" and len(self.points) == 4
            ):
                self.draw_shape()

    def draw_shape(self):
        if self.shape_type == "Triangle":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Square":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Circle":
            circle = plt.Circle(self.points[0], self.radius, color="black")
            self.ax.add_artist(circle)
        self.canvas.draw()

    def get_label(self):
        labels = {
            "Triangle": 0,
            "Square": 1,
            "Circle": 2,
        }
        return labels.get(self.shape_type, -1)

    def save(self, label):
        if self.shape_type == "Circle":
            coords = [*self.points[0], self.radius, 0, 0, 0, 0, 0]
        else:
            coords = [coord for point in self.points for coord in point]
            if self.shape_type == "Triangle" and len(self.points) == 3:
                coords.extend([0, 0])

        coords.append(label)
        print(",".join(map(str, coords)) + "\n")

        self.points.clear()
        self.radius = 0

    def clear_plot(self):
        self.ax.clear()
        self.configure_plot()
        self.points.clear()
        self.canvas.draw()

    def configure_plot(self):
        self.ax.set_xlim(0, 64)
        self.ax.set_ylim(0, 64)
