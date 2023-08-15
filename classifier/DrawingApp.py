import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from qiskit_machine_learning.algorithms.classifiers import VQC
import numpy as np


class DrawingApp:
    def __init__(self, master):
        self.master = master

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.onclick)
        self.master.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.shape_type = "Triangle"
        self.points = []
        self.radius = 0
        self.shape_completed = False

        # import the model
        self.vqc = None

        self.shape_var = tk.StringVar(value="Triangle")
        self.shapes_dropdown = tk.OptionMenu(
            master,
            self.shape_var,
            "Triangle",
            "Quadrilateral",
            "Circle",
            command=self.set_shape_from_dropdown,
        )
        self.shapes_dropdown.pack(side=tk.LEFT)
        btn_identify = tk.Button(master, text="Identify", command=self.on_identify)
        btn_identify.pack(side=tk.LEFT)

        self.shape_label = tk.Label(master, text="", width=30)
        self.shape_label.pack(side=tk.LEFT, padx=10)

        self.configure_plot()

    def load_model(self, vqc):
        self.vqc = vqc

    def quit_app(self):
        self.master.quit()  # Stop the main loop
        self.master.destroy()  # Destroy the main window

    def set_shape_from_dropdown(self, value):
        if value == "Triangle":
            self.set_triangle()
        elif value == "Quadrilateral":
            self.set_quadrilateral()
        elif value == "Circle":
            self.set_circle()

    def set_triangle(self):
        self.shape_completed = False
        self.shape_type = "Triangle"
        self.clear_plot()
        print("Switched to Triangle mode")

    def set_quadrilateral(self):
        self.shape_completed = False
        self.shape_type = "Quadrilateral"
        self.clear_plot()
        print("Switched to Quadrilateral mode")

    def set_circle(self):
        self.shape_completed = False
        self.shape_type = "Circle"
        self.clear_plot()
        print("Switched to Circle mode")

    def on_identify(self):
        if self.shape_type:
            label = self.get_label()
            self.identify(label)
            self.clear_plot()

    def onclick(self, event):
        if self.shape_completed:  # Check if shape is already completed
            return

        x, y = 0, 0
        try:
            x, y = round(event.xdata), round(event.ydata)
        except:
            print("Invalid point")
            return

        if self.shape_type == "Circle" and len(self.points) == 1:
            self.radius = int(
                ((x - self.points[0][0]) ** 2 + (y - self.points[0][1]) ** 2) ** 0.5
            )
            self.draw_shape()
        else:
            self.points.append((x, y))
            self.draw_temporary_shape()  # Draw temporary shape for visual feedback

            if (self.shape_type == "Triangle" and len(self.points) == 3) or (
                self.shape_type == "Quadrilateral" and len(self.points) == 4
            ):
                self.draw_shape()

    def draw_temporary_shape(self):
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                self.ax.plot(*zip(*self.points[i : i + 2]), color="grey")
        if len(self.points) > 0:
            self.ax.scatter(*self.points[-1], color="red", s=50)
        self.canvas.draw()

    def draw_shape(self):
        self.shape_completed = True
        if self.shape_type == "Triangle":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Quadrilateral":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Circle":
            circle = plt.Circle(self.points[0], self.radius, color="black")
            self.ax.add_artist(circle)
        self.canvas.draw()

    def get_label(self):
        labels = {
            "Triangle": 0,
            "Quadrilateral": 1,
            "Circle": 2,
        }
        return labels.get(self.shape_type, -1)

    def identify(self, label):
        if self.shape_type == "Circle":
            coords = [*self.points[0], self.radius, 0, 0, 0, 0, 0]
        else:
            coords = [coord for point in self.points for coord in point]
            if self.shape_type == "Triangle" and len(self.points) == 3:
                coords.extend([0, 0])

        coords.append(label)

        # create target and label
        data = list(map(int, map(str, coords)))
        target = np.array(data[:-1])
        label = np.array(data[-1])

        if len(target) != 8:
            print("Invalid shape")
            return

        prediction = self.vqc.predict(target)
        if prediction == 0:
            self.shape_label.config(
                text="Prediction: Triangle, Actual: " + self.shape_type
            )
        elif prediction == 1:
            self.shape_label.config(
                text="Prediction: Quadrilateral, Actual: " + self.shape_type
            )
        elif prediction == 2:
            self.shape_label.config(
                text="Prediction: Circle, Actual: " + self.shape_type
            )

        self.points.clear()
        self.radius = 0

    def clear_plot(self):
        self.shape_completed = False
        self.ax.clear()
        self.configure_plot()
        self.points.clear()
        self.canvas.draw()

    def configure_plot(self):
        self.ax.set_xlim(0, 64)
        self.ax.set_ylim(0, 64)
