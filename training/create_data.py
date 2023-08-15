import matplotlib.pyplot as plt


class create_data:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        plt.xlim(0, 64)
        plt.ylim(0, 64)
        self.shape_type = None
        self.points = []
        self.radius = 0
        self.cid_press = self.fig.canvas.mpl_connect("button_press_event", self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect("key_press_event", self.onkey)
        plt.show()

    def onclick(self, event):
        x, y = round(event.xdata), round(event.ydata)  # Round to int

        if self.shape_type == "Circle" and len(self.points) == 1:
            self.radius = int(
                ((x - self.points[0][0]) ** 2 + (y - self.points[0][1]) ** 2) ** 0.5
            )
            self.draw_shape()
        else:
            self.points.append((x, y))

            # Check if enough points have been clicked to draw the shape
            if (self.shape_type == "Triangle" and len(self.points) == 3) or (
                self.shape_type == "Square" and len(self.points) == 4
            ):
                self.draw_shape()

    def onkey(self, event):
        if event.key == "1":
            self.shape_type = "Triangle"
            self.clear_plot()
            print("Switched to Triangle mode")
        elif event.key == "2":
            self.shape_type = "Square"
            self.clear_plot()
            print("Switched to Square mode")
        elif event.key == "3":
            self.shape_type = "Circle"
            self.clear_plot()
            print("Switched to Circle mode")
        elif event.key == "enter":
            if self.shape_type:
                label = self.get_label()
                self.save(label)
                print(f"Saved {self.shape_type} with label {label}")
                self.clear_plot()

    def draw_shape(self):
        if self.shape_type == "Triangle":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Square":
            self.ax.fill(*zip(*self.points), color="black")
        elif self.shape_type == "Circle":
            circle = plt.Circle(self.points[0], self.radius, color="black")
            self.ax.add_artist(circle)
        plt.draw()

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
        with open("training/shapes.txt", "a") as f:
            f.write(",".join(map(str, coords)) + "\n")

        self.points.clear()
        self.radius = 0

    def clear_plot(self):
        self.ax.clear()
        plt.xlim(0, 64)
        plt.ylim(0, 64)
        self.points.clear()
        plt.draw()


app = create_data()
