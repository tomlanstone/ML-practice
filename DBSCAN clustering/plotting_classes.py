import csv
import webbrowser

import folium

class Point:
    def __init__(self, lat, long, cluster, color):
        self.lat = lat
        self.long = long
        self.cluster = cluster
        self.color = color

class Map:
    def __init__(self, points):
        self.points = points
        self.mid = self.find_mid_point()
        self.map = folium.Map(location=self.mid, zoom_start=6.2)

    def find_mid_point(self):
        lats = [p.lat for p in self.points]
        longs = [p.long for p in self.points]
        return [sum(lats) / len(lats), sum(longs) / len(longs)]

    def add_points_to_map(self):
        for point in self.points:
            label = f"{point.lat}, {point.long} <br><br>{point.cluster}: {point.color}"
            iframe = folium.IFrame(label)
            popup = folium.Popup(iframe, min_width=400, max_width=400, min_height=0, max_height=100)
            folium.CircleMarker(location=[point.lat, point.long], radius=5, color=point.color, popup=popup).add_to(self.map)

        folium.CircleMarker(location=self.mid, radius=10, color='green', popup="mid point").add_to(self.map)

    def save_map(self, file_name):
        self.map.save(file_name)
    
    def view_map(self): ## not functiooning correctly, figure out later
        map_html = self.get_root().render()
        webbrowser.open("data:text/html;charset=utf-8," + map_html)

def open_map_from_file(file_name):
    webbrowser.open(file_name)

def read_points_from_csv(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip the header row
        points = []
        for row in reader:
            lat = float(row[0])
            long = float(row[1])
            cluster = row[2]
            color = row[3]
            points.append(Point(lat, long, cluster, color))
    return points

points = read_points_from_csv("DBSCAN_output.csv")
map = Map(points)
map.add_points_to_map()
map.view_map()

