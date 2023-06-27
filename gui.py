from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class GUI:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self._setup_window()
        self.quit_button = ttk.Button(self.root, text="Generate Graphs", command=lambda: self.root.config(theme="breeze"))
        self.quit_button.pack(column=3, row=5)

    def run(self):
        self.root.mainloop()

    def _setup_window(self):
        self.root.title("Pymograph")
        self.root.geometry("680x420")
        self.root.minsize(300, 300)
        graph = matplotlib.pyplot