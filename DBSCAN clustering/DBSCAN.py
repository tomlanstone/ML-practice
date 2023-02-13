import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.distance import geodesic

# Function to calculate the Euclidean distance between two points
def distance_calculator(p1, p2, method):
    if method.lower() == "euclidean": return np.sqrt(np.sum((p1 - p2)**2))
    if method.lower() == "geo": return geodesic(p1, p2).km

# DBSCAN class
class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5, distance_method = "Euclidean"):
        # eps is the maximum distance between two samples for them to be considered as part of the same cluster
        self.eps = eps
        # min_samples is the minimum number of samples in a neighborhood around a sample for it to be considered a core sample
        self.min_samples = min_samples

        self.distance_method = distance_method
        
    def fit(self, X):
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
            neighbors = self._region_query(i)
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
                neighbors2 = self._region_query(j)
                if len(neighbors2) >= self.min_samples:
                    neighbors = np.union1d(neighbors, neighbors2)
                    
    # Helper function to find the neighbors of a sample within a distance of eps
    def _region_query(self, p):
        neighbors = []
        for i in range(self.X.shape[0]):
            # Check if the sample is within a distance of eps from the current sample        
            if distance_calculator(self.X[p], self.X[i],  self.distance_method) <= self.eps:
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

## Assign colours based on cluster number
def number_to_color(number, cmap_name='rainbow'):
    cmap = plt.get_cmap(cmap_name)
    if float(number) <0:
        colour = "black"
    else:
        colour = cmap(number)
    return colour

## Convert the colour to hex cos the plotter gets upset by cmap colours
def rgba_to_hex(rgba):
    try:
        r, g, b, a = rgba
        hex_colour = '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
        return hex_colour
    except:
        return '#000000'

def read_data_csv(file_name, headers = True):
    ## Read in data from csv
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        if headers == True: header = next(reader) # skip the header row
        data = []
        for row in reader:
            new_row = []
            for i in row:
                new_row.append(float(i))
            data.append(new_row)
    ## Output as a Numpy Array for the model to use 
    return np.array(data)

## Initiate model for global data
full_globe = DBSCAN(eps=30, min_samples=4, distance_method = "geo")
uk = DBSCAN(eps = 50, min_samples= 2, distance_method = "geo")

## Fit the data to the model
data = read_data_csv("UK.csv", headers = True)
full_globe.fit(data)
uk.fit(data)
def build_map_input(model, data):
    df = pd.DataFrame(columns=('Latitude','Longitude','Cluster','Colour'))
    df['Latitude'] = [i[1] for i in data]
    df['Longitude'] = [i[0] for i in data]
    df['Cluster'] = model.labels_
    df['Colour'] =  [(rgba_to_hex(number_to_color(i/max(df['Cluster']),"rainbow"))) for i in df['Cluster']]
    save_output(df, "DBSCAN_output.csv")

build_map_input(uk,data)
