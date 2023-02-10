import numpy as np
import pandas as pd
import csv

def generate_random_coordinates(n = 100, x_min = -180, x_max = 180, y_min = -90, y_max = 90):
    x = np.random.uniform(x_min, x_max, size=n)
    y = np.random.uniform(y_min, y_max, size=n)
    return pd.DataFrame(np.column_stack((x, y)))

def save_coords(dataframe,name):
    with open(name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["y", "x"])
        for row in dataframe.to_numpy():
            writer.writerow(row)

coordinates = generate_random_coordinates(n = 150)

save_coords(coordinates,"coordinates.csv")