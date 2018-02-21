1. Prerequisites.
 - OS: tested on Linux Fedora 24;
 - Python 3.5.3 or higher;
 - Flask 0.12.2 or higher;
 - Pillow 5.0.0

2. Start the application:

	python netcdf_polygon_selector.py

	Make sure that the application has been started successfully.

3. Open the properties.py file and specify the actual parameters values.

	source_path - path to netcdf4 source file directory.
	target_path - path where output images will be placed
	out_file_name - output image name (without extension)
	zoom - necessary zoom level

4. In a browser address line put the request:

	http://127.0.0.1:5000/v1/get_site?c=-1023403,-942814,-969723,-903774,-936783,-958674,-962403,-1003814,-1027063,-995274,-1023403,-942814&fn=sigma0_hh.nc
	
	Params: c - coordinates, fn - file name (both are required)

5. In current version you will receive the output image full path as request.
