import numpy as np
from geopy.distance import geodesic
import csv

def generate_random_coordinates(n, x_min, x_max, y_min, y_max):
    x = np.random.uniform(x_min, x_max, size=n)
    y = np.random.uniform(y_min, y_max, size=n)
    return np.column_stack((x, y))

coordinates = generate_random_coordinates(100, 0, 100, 0, 100)

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

X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])

dbscan = DBSCAN(eps=3, min_samples=2)
dbscan.fit(coordinates)

print(dbscan.labels_)

## Write coordinates to csv for the plotter to plot on the map - later will need to make the script able to do the plotting itself and include cluster identification
with open("coordinates.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["y", "x"])
    for row in coordinates:
        writer.writerow(row)