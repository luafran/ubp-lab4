import logging
import os
import uuid

from base64 import decodestring
from bottle import Bottle, run, request, static_file

LISTEN_PORT = 8083

logger = logging.getLogger('storage-svc')
logger.setLevel(logging.DEBUG)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

BASE_DIR = os.path.join(os.path.dirname(__file__))
STATIC_FILES_DIR = os.path.join(BASE_DIR, "static")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")


app = Bottle()


@app.route('/test', method='GET')
def get_test():
    logger.info('Processing GET /test')
    retdata = {
        "status": "OK"
    }
    return retdata


@app.route('/')
def home():
    return static_file('upload.html', root=STATIC_FILES_DIR)


@app.route('/file/<filename>')
def serve_storage(filename):
    return static_file(filename, root=STORAGE_DIR)


@app.route('/file', method='POST')
@app.route('/file/', method='POST')
def do_upload():
    data = request.json
    logger.info("receiving file...")

    base64 = data["content"]

    content_type = data["contentType"]
    logger.debug("content_type: {0}".format(content_type))
    file_ext = '.{0}'.format(content_type.split('/')[1])

    if file_ext not in ('.png', '.jpg', '.jpeg'):
        error_data = {
            "status": "ERROR",
            "message": "File extension not allowed."
        }
        return error_data

    file_id = str(uuid.uuid4())
    file_name = file_id + file_ext
    save_path = os.path.join(STORAGE_DIR, file_name)
    with open(save_path, "wb") as f:
        f.write(decodestring(base64))

    retdata = {
        "status": "OK",
        "fileId": file_name
    }

    return retdata

logger.info('Starting Storage Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
