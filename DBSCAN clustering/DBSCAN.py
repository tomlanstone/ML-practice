import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.distance import geodesic


def generate_random_coordinates(n, x_min, x_max, y_min, y_max):
    x = np.random.uniform(x_min, x_max, size=n)
    y = np.random.uniform(y_min, y_max, size=n)
    return np.column_stack((x, y))


# Function to calculate distance between coordinates
def geo_distance(p1, p2):
    return geodesic(p1, p2).km

# Function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# DBSCAN class
class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        # eps is the maximum distance between two samples for them to be considered as part of the same cluster
        self.eps = eps
        # min_samples is the minimum number of samples in a neighborhood around a sample for it to be considered a core sample
        self.min_samples = min_samples
        
    def fit(self, X, geo = False):
        # Store the input data
        self.X = X
        # Initialize the labels to -1, indicating that they haven't been assigned to a cluster yet
        self.labels_ = np.zeros(X.shape[0], dtype=int)
        self.labels_.fill(-1)
        
        # Counter for the number of clusters
        C = 0
        for i in range(X.shape[0]):
            # If the sample has already been assigned a label, skip it
            if self.labels_[i] != -1:
                continue
                
            # Find the neighbors of the sample
            neighbors = self._region_query(i, geo)
            # If the number of neighbors is less than the minimum required, mark it as noise
            if len(neighbors) < self.min_samples:
                self.labels_[i] = -1
                continue
                
            # If the number of neighbors is greater than or equal to the minimum required, start a new cluster
            C += 1
            self.labels_[i] = C
            self.labels_[neighbors] = C
            
            # Expand the cluster to include all neighboring samples that are also core samples
            for j in neighbors:
                neighbors2 = self._region_query(j, geo)
                if len(neighbors2) >= self.min_samples:
                    neighbors = np.union1d(neighbors, neighbors2)
                    
    # Helper function to find the neighbors of a sample within a distance of eps
    def _region_query(self, p, geo = False):
        neighbors = []
        for i in range(self.X.shape[0]):
            # Check if the sample is within a distance of eps from the current sample
            if geo == True:
                if geo_distance(self.X[p], self.X[i]):
                    neighbors.append(i)
            if geo == False:        
                if euclidean_distance(self.X[p], self.X[i]) <= self.eps:
                    neighbors.append(i)
                
        # Return the array of indices of the neighboring samples
        return np.array(neighbors)

## Write coordinates to csv for the plotter to plot on the map - later will need to make the script able to do the plotting itself and include cluster identification
def save_output(dataframe,name):

    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["y", "x", "cluster", "colour"])
        for row in dataframe.to_numpy():
            writer.writerow(row)
            #print(row)

def number_to_color(number, cmap_name='viridis'):
    cmap = plt.get_cmap(cmap_name)
    color = cmap(number)
    return color
    
def rgba_to_hex(rgba):
    r, g, b, a = rgba
    hex_color = '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
    return hex_color

X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])
coordinates = generate_random_coordinates(100, -180, 180, -90, 90)

dbscan = DBSCAN(eps=30, min_samples=4)
dbscan.fit(coordinates)

clusters = dbscan.labels_


X = coordinates
lat = [i[1] for i in X]
long = [i[0] for i in X]
colours = []
for i in clusters:
    colours.append(rgba_to_hex(number_to_color(i/max(clusters),"rainbow")))



plt.get_cmap('rainbow')(clusters / max(clusters))

df = pd.DataFrame(columns=('Latitude','Longitude','Cluster','Colour'))
df['Latitude'] = lat
df['Longitude'] = long
df['Cluster'] = clusters
df['Colour'] = colours

save_output(df, "coordinates.csv")