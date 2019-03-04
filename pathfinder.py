from PIL import Image
from random import choice
import argparse
from time import time


class ElevationMap:
    """
    An elevation map takes a text file with each line having numerical values representing elevations separated
    by spaces.  It strips that data into lists and dictionaries and stores important values about the map.
    Has useful methods for getting elevation data for each coordinate.
    """


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
        # self.coords_dict = {}
        # for y in range(self.height):
        #     for x in range(self.width):
        #         self.coords_dict[(x, y)] = self.elevation_graph[y][x]

    def get_elevation(self, x, y):
        """Returns the elevation at a given x, y coordinate."""
        return self.elevation_graph[y][x]

    def get_elevation_intensity(self, x, y, scale):
        """Given an x, y coordinate, represent the elevation as a ratio of the range of given elevations,
        and then scale it to the given scale. ie: range of elevations = 200-300, scale = 1000, elevation
        at the given point is 233, return 330."""
        return int(((self.get_elevation(x, y) - self.min_elevation) / self.elevation_range) * scale)

    def get_diff(self, x, y, a, b):
        """Given two coordinate, return the difference in elevations at each coordinate."""
        return abs(self.get_elevation(x, y)-self.get_elevation(a, b))


class PointDrawer:
    """
    A PointDrawer has methods to represent elevation maps as images and 
    draw paths of coordinates on images.
    """


    def __init__(self):
        pass

    def draw_emap(self, emap):
        """Given an ElevationMap, draw each point in gray scale with an intensity that matches its
        percentage of the total range of elevation.  Higher points == lighter, lower points == darker."""
        my_mountain = Image.new('RGB', (emap.width, emap.height), (255,255,255))
        for y in range(emap.height):
            for x in range(emap.width):
                rgb_value = emap.get_elevation_intensity(x, y, 255)
                my_mountain.putpixel((x, y), (rgb_value, rgb_value, rgb_value))
        return my_mountain

    def draw_path(self, path, image, rgb):
        """Given a list of coordinates (path), draw a pixel on an image with the rgb value given."""
        for coord in path:
            image.putpixel(coord, rgb)


class PathFinder:
    """
    A PathFinder takes an ElevationMap as its main argument.  It has methods to find 'paths of least resistance'
    from different points on the map.
    """


    def __init__(self, emap):
        self.emap=emap

    def find_greedy_step(self, x, y):
        """Given a coordinate, return a coordinate to the right and either up, straight, or down
        one from the starting coordinate that causes the least change in elevation."""
        if y == 0:
            options = [y,y+1]
            diffs = [self.emap.get_diff(x,y,x+1,y),self.emap.get_diff(x,y,x+1,y+1)]
        elif y == self.emap.height - 1:
            options = [y,y-1]
            diffs = [self.emap.get_diff(x,y,x+1,y),self.emap.get_diff(x,y,x+1,y-1)]
        else:
            options = [y,y-1,y+1]
            diffs = [self.emap.get_diff(x,y,x+1,y),self.emap.get_diff(x,y,x+1,y-1),self.emap.get_diff(x,y,x+1,y+1)]
        best_option_index = diffs.index(min(diffs))
        best_option = options[best_option_index]
        if best_option_index>0 and len(options)==3 and diffs[1]==diffs[2]:
            best_option = choice([y+1, y-1])
        return (x+1, best_option)

    def find_greedy_path(self, y):
        """Given a starting y value, return a list of coordinates that represents the path where each step
        is the step that causes the least change in elevation."""
        greedy_path = [(0, y)]
        for x in range(self.emap.width-1):
            best_way_forward = self.find_greedy_step(x,y)
            greedy_path.append(best_way_forward)
            y = best_way_forward[1]
        return greedy_path

    def find_greediest_path(self, y_range):
        """Given a range of y values, generates a list of greedy paths using each y value as a starting point,
        and then returns the path with the least total change in elevation."""
        paths = [self.find_greedy_path(y) for y in y_range]
        min_path = min(paths, key=lambda k: self.get_path_ediff(k))
        return min_path
        
    def get_path_ediff(self, path):
        """Given a path (ordered list of coordinates), return the sum of the difference
        in elevation between each step of the path."""
        total_ediff = 0
        for i in range(len(path)-1):
            total_ediff += self.emap.get_diff(path[i][0], path[i][1], path[i+1][0], path[i+1][1])
        return total_ediff
    
    def find_best_path(self, x, y):
        """Given a coordinate, find the path with the least elevation change from that coordinate
        to the right side of the map"""
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help = "The file path for the elevation map data")
    args = parser.parse_args()

    emapinit_time = time()
    emap = ElevationMap(args.file)
    print(f"Emap Init: {time()-emapinit_time}")

    pdrawerinit_time = time()
    point_drawer = PointDrawer()
    print(f"Pdrawer Init: {time()-pdrawerinit_time}")

    drawemap_time = time()
    my_image = point_drawer.draw_emap(emap)
    print(f"Draw Emap: {time()-drawemap_time}")

    pfinderinit_time = time()
    pathfinder = PathFinder(emap)
    print(f"Pfinder Init: {time()-pfinderinit_time}")

    findgreediestpath_time = time()
    greedy_path = pathfinder.find_greediest_path(range(emap.height))
    print(f"Find Greediest Path: {time()-findgreediestpath_time}")

    drawpath_time = time()
    point_drawer.draw_path(greedy_path, my_image, (0,255,0))
    print(f"Draw Path: {time()-drawpath_time}")

    my_image.save("my_pretty_mountain.png")
