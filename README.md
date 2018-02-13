1. Prerequisites.
 - OS: tested on Linux Fedora 24;
 - Python 3.5.3 or higher;
 - Redis 3.2.8 or higher;
 - Py-redis 2.10.3 or higher;
 - Flask 0.12.2 or higher;
 - Python RQ 0.10.0 or higher;
 - Pillow 5.0.0

Clone the repository to some local directory (/path/to/application/).

Execute the next step from repo directory (/path/to/application/).

2. Deploy platform and application.
 - Make sure that all prerequisites are satisfied.
 - Start Redis server.
    E.g. for RH-like:
      
	sudo service redis start

 - Start RQ workers.

    RQ is a simple Python library for queueing jobs and processing them in the background with workers.
    Each worker will process a single job at a time. If you want to perform jobs concurrently, simply start more workers.

    It is recommended to use background mode and nohup logging to start RQ workers.

    RQ workers startup using default settings (run it twice to have two running jobs at the same time):

    nohup rq worker &

    Check nohup log for any issues.

 - Start the application.

    It is recommended to use background mode and nohup logging to start RQ workers.

    nohup ./netcdf_polygon_selector.py &

    Check nohup log for any issues.
    If anything is OK you will see something like

    22:48:00 RQ worker 'rq:worker:numenor.6023' started, version 0.10.0
22:48:00 *** Listening on default...
22:48:00 Cleaning registries for queue: default
22:48:02 RQ worker 'rq:worker:numenor.6038' started, version 0.10.0
22:48:02 *** Listening on default...
22:48:02 Cleaning registries for queue: default
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 523-202-160

3. Usage.

 - Input data.
	
    In your working directory create 'data/' subdirectory and put your netcdf data file there.

    =========================================================================
    |   IMPORTANT! The service has been tested with NetCDF version 4 only.  |
    =========================================================================

    To start poligon site creation execute the POST request:

    request:
	[isilme@numenor netcdf4_project]$ curl -i -H "Content-Type: application/json" -X POST -d '{"file_name":"sigma0_hh.nc","coordinates":"-1453097,-622420,-1365292,-546145,-1259748,-617099,-1259748,-728851,-1351988,-772310,-1461080,-731512,-1453097,-622420"}' http://127.0.0.1:5000/v1/get_site

	Where:
		- file_name - your netcdf file in ./data directory
		- coordinates - polygon coordinates (meters)

    response:

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 57
Server: Werkzeug/0.14.1 Python/3.5.3
Date: Tue, 13 Feb 2018 21:57:21 GMT

{
  "Job_UUID": "34cde852-7ad6-4d2b-be75-cdd8f18bd9f1"
}


    To show result:

    Use Job_UUID from previous point to get job status:

    request:
	[isilme@numenor netcdf4_project]$ curl -i -H "Content-Type: application/json" -X GET -d '{"task_uuid":"10c0a799-7354-4f17-8ede-41355fc88d87"}' http://127.0.0.1:5000/v1/get_site


    response:
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 64
Server: Werkzeug/0.14.1 Python/3.5.3
Date: Tue, 13 Feb 2018 21:57:53 GMT

{
  "Result": "./data/tile_site.png", 
  "Status": "\"DONE\""
}

	Where:
		- Result - output image


