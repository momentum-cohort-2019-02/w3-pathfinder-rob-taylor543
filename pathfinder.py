from PIL import Image
from random import choice


class ElevationMap:


    def __init__(self, file):
        self.elevation_graph = []
        with open(file) as the_file:
            for line in the_file.readlines():
                self.elevation_graph.append([int(e) for e in line.split()])
        self.max_elevation = max([max(e) for e in self.elevation_graph])
        self.min_elevation = min([min(e) for e in self.elevation_graph])
        self.elevation_range = self.max_elevation - self.min_elevation
        self.width = len(self.elevation_graph[0])
        self.height = len(self.elevation_graph)
        self.coords_dict = {}
        for y in range(self.height):
            for x in range(self.width):
                self.coords_dict[(x, y)] = self.elevation_graph[y][x]

    def get_elevation(self, x, y):
        return self.elevation_graph[y][x]

    def get_elevation_intensity(self, x, y, scale):
        return int(((self.get_elevation(x, y) - self.min_elevation) / self.elevation_range) * scale)

    def get_elevation_difference(self, x, y, a, b):
        return abs(self.get_elevation(x, y)-self.get_elevation(a, b))

    def draw_elevation_map(self):
        my_mountain = Image.new('RGB', (len(self.elevation_graph), len(self.elevation_graph[0])), (255,255,255))
        for y in range(len(self.elevation_graph)):
            for x in range(len(self.elevation_graph[0])):
                rgb_value = self.get_elevation_intensity(x, y, 255)
                my_mountain.putpixel((x, y), (rgb_value, rgb_value, rgb_value))
        return my_mountain

    def find_best_way_forward(self, x, y):
        if y == 0:
            options = {(x+1, y):self.get_elevation_difference(x,y,x+1,y),(x+1, y+1):self.get_elevation_difference(x,y,x+1,y+1)}
        elif y == self.height - 1:
            options = {(x+1, y-1):self.get_elevation_difference(x,y,x+1,y-1),(x+1, y):self.get_elevation_difference(x,y,x+1,y)}
        else:
            options = {(x+1, y-1):self.get_elevation_difference(x,y,x+1,y-1),(x+1, y):self.get_elevation_difference(x,y,x+1,y),(x+1, y+1):self.get_elevation_difference(x,y,x+1,y+1)}
        best_option = (x+1, y)
        best_option = min(options, key = options.__getitem__)
        if (len(options) == 3) and (not best_option == (x+1, y)) and (options[(x+1,y-1)] == options[(x+1,y+1)]):
            best_option = choice([(x+1, y-1), (x+1, y+1)])
        return best_option, self.get_elevation_difference(x,y,best_option[0],best_option[1])

    def draw_greedy_path(self, y_value):
        my_mountain_image = self.draw_elevation_map()
        total_elevation_changes = {}
        for start_y in y_value:
            y = start_y
            total_elevation_change = 0
            for x in range(len(self.elevation_graph[0])-1):
                best_way_forward, elevation_change = self.find_best_way_forward(x,y)
                my_mountain_image.putpixel(best_way_forward, (240,240,240))
                y = best_way_forward[1]
                total_elevation_change += elevation_change
            total_elevation_changes[start_y] = total_elevation_change
        min_elevation_change_y = sorted(total_elevation_changes, key = total_elevation_changes.__getitem__)[0]
        for x in range(len(self.elevation_graph[0])-1):
            best_way_forward = self.find_best_way_forward(x,min_elevation_change_y)[0]
            my_mountain_image.putpixel(best_way_forward, (0,255,0))
            min_elevation_change_y = best_way_forward[1]
        return my_mountain_image


class PointDrawer:


    def __init__(self, elevation_map):
        self.elevation_map = elevation_map


my_mountain = ElevationMap("elevation_small.txt")
my_image = my_mountain.draw_greedy_path(range(600))
my_image.save("my_pretty_mountain.png")


