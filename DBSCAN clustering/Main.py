import tkinter as tk
from tkinter import ttk

from DBSCAN import *
from example_coords_generator import *
from plotter import *


def execfile(file_name):
    exec(open(file_name).read())

## Get new coordinates
execfile("example_coords_generator.py")
## Apply clustering model
execfile("DBSCAN.py")
## Map the clusters
execfile("plotter.py")

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Application")
        #self.geometry("300x200")
        webview = ttk.Webview(self, width=800, height=600)
        webview.pack()
        webview.set_html("<h1>Hello World!</h1>")

#root = root()
#root.mainloop()

