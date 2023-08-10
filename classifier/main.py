from DrawingApp import DrawingApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    app = DrawingApp(root)
    root.mainloop()
