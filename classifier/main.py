from DrawingApp import DrawingApp
import tkinter as tk
from qiskit_machine_learning.algorithms.classifiers import VQC

vqc = VQC.load("vqc.model")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("720x720")
    app = DrawingApp(root)
    app.load_model(vqc)
    root.mainloop()
