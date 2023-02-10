import csv
import webbrowser

import folium

coordinates = []
with open("coordinates.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader) # skip the header row
    for row in reader:
        lat = float(row[0])
        long = float(row[1])
        cluster = row[2]
        colour = row[3]
        coordinates.append([lat,long,cluster,colour])
    
## Formula for mean of a list
def list_mean(x):
    return sum(x)/len(x)

## Calculate mid point of coordinates
def find_mid_point(points):
    lats = [i[0] for i in points]
    longs = [i[1] for i in points]
    mid = [list_mean(lats), list_mean(longs)]
    return mid
    

## Function to plot points on a map
## Later on, when adapted to work with data from csv, change the labeller to take in something useful like sampleEventID 
def plot_points_on_map(points):
    mid = find_mid_point(points)
    map = folium.Map(location=mid, zoom_start=2) # center the map on UK
    count = 1
    for point in points:
        lat, long, cluster, colour = point
        label = f"{lat}, {long} <br><br>{cluster}: {colour}"
        iframe = folium.IFrame(label)
        popup = folium.Popup(iframe, min_width=400,  max_width=400, min_height = 00, max_height = 100)
        folium.CircleMarker(location=[lat, long], radius=5, color=colour, popup=popup).add_to(map)
        count += 1
    folium.CircleMarker(location=mid, radius=10, color='green', popup= "mid point").add_to(map)
    return map

map = plot_points_on_map(coordinates)
map_name = "Locations.html"
map.save(map_name)
webbrowser.open(map_name)





