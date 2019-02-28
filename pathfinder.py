from PIL import Image

with open("elevation_large.txt") as file:
    elevation_graph = []

    first_row = file.readline()
    first_row_split = first_row.split()

    largest_elevation = 0
    smallest_elevation = 20000

    for elevation in first_row.split():
        elevation_graph.append([int(elevation)])
        if int(elevation) > largest_elevation:
            largest_elevation = int(elevation)
        if int(elevation) < smallest_elevation:
            smallest_elevation = int(elevation)
    
    for line in file.readlines():
        x = 0
        split_row = line.split()
        for elevation in split_row:
            elevation_graph[x].append(int(elevation))
            if int(elevation) > largest_elevation:
                largest_elevation = int(elevation)
            if int(elevation) < smallest_elevation:
                smallest_elevation = int(elevation)
            x+=1


my_mountain = Image.new('RGB', (len(elevation_graph), len(elevation_graph[0])), (255,255,255))

elevation_range = largest_elevation - smallest_elevation


for y in range(len(elevation_graph)):
    for x in range(len(elevation_graph)):
        color_percent = (elevation_graph[x][y] - smallest_elevation) / elevation_range
        rgb_value = int(color_percent*255)
        my_mountain.putpixel((x, y), (rgb_value, rgb_value, rgb_value))

my_mountain.save('my_pretty_mountain.jpg')
