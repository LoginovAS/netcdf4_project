from netCDF4 import Dataset
import numpy as np
from PIL import Image, ImageDraw, ImageOps

target_path = "./data/"
out_file_name = 'tile_site.png'

def draw_polygon(file_name, coords):

    nc_file = target_path + file_name
    nc_dataset = Dataset(nc_file, 'r')

    # Take necessary parameters from file
    bbox_lat_min = getattr(nc_dataset, 'bbox_lat_min')
    bbox_lon_min = getattr(nc_dataset, 'bbox_lon_min')
    bbox_lat_max = getattr(nc_dataset, 'bbox_lat_max')
    bbox_lon_max = getattr(nc_dataset, 'bbox_lon_max')
    resolution = int(float(getattr(nc_dataset, 'resolution')))

    width = (bbox_lon_max - bbox_lon_min) // resolution

    def coords_to_num(line):
        ar = []
        for c in line:
            ar.append(float(c))

        return ar

    def line_to_tuple(*line, count):
        return tuple(zip(*[iter(coords_to_num(line))] * count))

    def get_array_coords(meters_coords):
        xy = []
        for coord in meters_coords:
            temp = tuple([int(abs((bbox_lat_min - coord[0]) // resolution)),
                  width - int(abs((bbox_lon_min - coord[1]) // resolution))])
            xy.append(temp)
        return tuple(xy)

    array_coords = (get_array_coords(line_to_tuple(*coords, count = 2)))

    tile_array = nc_dataset.variables["Data"][6]

    xy = tile_array.shape

    poly = Image.new('L', xy, (255))
    tile = Image.fromarray(tile_array, 'L')

    draw = ImageDraw.Draw(poly)
    draw.polygon(list(array_coords), outline = 1, fill=0)

    tile.paste(poly, (0,0), mask = poly)


    tile.save(target_path + out_file_name, 'PNG')

    return target_path + out_file_name
