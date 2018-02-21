from netCDF4 import Dataset
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from datetime import datetime

source_path = "/home/isilme/python/python/solab/data/S1B_EW_GRDM_1SDH_20171218T133056_20171218T133156_008774_00F9DD_335B/"
target_path = "/home/isilme/python/python/solab/data/"
out_file_name = 'tile_site'

def draw_polygon(file_name, coords):

    nc_file = source_path + file_name
    nc_dataset = Dataset(nc_file, 'r')

    # Take necessary parameters from file
    bbox_lat_min = int(getattr(nc_dataset, 'bbox_lat_min'))
    bbox_lon_min = int(getattr(nc_dataset, 'bbox_lon_min'))
    bbox_lat_max = int(getattr(nc_dataset, 'bbox_lat_max'))
    bbox_lon_max = int(getattr(nc_dataset, 'bbox_lon_max'))
    resolution = int(float(getattr(nc_dataset, 'resolution')))

    height = (bbox_lon_max - bbox_lon_min) // resolution

    def get_array_coords(meters_coords):
        meters_coords[::2] = (meters_coords[::2] - bbox_lat_min) // resolution
        meters_coords[1::2] = -(meters_coords[1::2] - bbox_lon_min - height*resolution) // resolution
        return meters_coords

    np_ar = np.asarray(coords, dtype=np.int32)

    array_coords = get_array_coords(np_ar)

    tile_array = nc_dataset.variables["Data"][6]

    xy = tile_array.shape

    poly = Image.new('L', xy, (255))
    tile = Image.fromarray(tile_array, 'L')

    draw = ImageDraw.Draw(poly)
    draw.polygon(list(array_coords), outline = 1, fill=0)

    tile.paste(poly, (0,0), mask = poly)

    out_file_fullname = target_path + out_file_name + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    tile.save(out_file_fullname, 'PNG')

    return out_file_fullname
