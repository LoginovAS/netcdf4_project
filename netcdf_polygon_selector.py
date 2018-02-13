import json
from flask import Flask, jsonify, abort
from flask import make_response, request, url_for
import netcdf_service as ns
from status import JobStatus

app = Flask(__name__)

@app.route('/v1/get_site', methods=['POST'])
def get_polygon_site():
    coords = request.json['coordinates'].split(',')
    file_name = request.json['file_name']
    print(coords)
    job_id = ns.create_task(coords, file_name)
    return jsonify({'Job_UUID':job_id}), 201

@app.route('/v1/get_site', methods=['GET'])
def get_task():
    job_id = request.json['task_uuid']

    job = ns.get_task(job_id)

    if job.is_failed:
        return jsonify({'Status':json.dumps(JobStatus.ERROR.name),'Result':job.exc_info}), 204

    if job.is_finished:
        return jsonify({'Status':json.dumps(JobStatus.DONE.name),'Result':job.result}), 200

    if job.is_started:
        return jsonify({'Status':json.dumps(JobStatus.RUNNING.name),'Result':''}), 200

    if job.is_queued:
        return jsonify({'Status':json.dumps(JobStatus.QUEUED.name),'Result':''}), 200

if __name__ == '__main__':
    app.run(debug = True)
