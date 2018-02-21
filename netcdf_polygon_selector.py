import json
from flask import Flask, render_template
from flask import make_response, request, url_for
import netcdf_tasks as nt
from status import JobStatus
import os

app = Flask(__name__)
IMAGE_FOLDER = '/home/isilme/python/python/solab/data/'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

@app.route('/v1/get_site', methods=['GET'])
def get_polygon_site():
    coords = request.args.get('c').split(',')
    file_name = request.args.get('fn')
    print(coords)
    image = nt.draw_polygon(file_name, coords)
    # full_filename = os.path.join(app.config['IMAGE_FOLDER'], 'tile_site.png')
    # return render_template("image.html", site_image = full_filename)
    return image

if __name__ == '__main__':
    app.run(debug = True)
