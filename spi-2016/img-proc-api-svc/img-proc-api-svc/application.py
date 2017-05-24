import json
import logging
import os
import time
import uuid

from bottle import Bottle, run, request
import pika
import pymysql

LISTEN_PORT = 8082

logger = logging.getLogger('img-proc-api-svc')
logger.setLevel(logging.DEBUG)
logger.propagate = False
# create file handler
# fh = logging.FileHandler('img-proc-api-svc.log')
# fh.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)


TAG_ORIGINAL_IMAGE_URL = 'originalImageUrl'
TAG_FILTER_ID = 'filterId'
TAG_RESULT_IMAGE_URL = 'resultImageUrl'
TAG_STATUS = 'status'
TAG_JOB_ID = 'jobId'

QUEUE_NAME = 'task_queue'


mysql_config = {
    'host': 'mysql',
    'user': os.environ['MYSQL_USER'],
    'passwd': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE']
}


app = Bottle()


def init_db():
    """
    DB INIT
    """
    logger.info('Processing init database')

    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()

        create_db = "create database if not exists spi"
        cursor.execute(create_db)

        create_table = "create table if not exists spi.jobs(user_id varchar(25)," \
                       "job_id varchar(50), status varchar(25)," \
                       "original_image_url varchar(100), filter_id varchar(50)," \
                       "result_image_url varchar(100))"
        cursor.execute(create_table)
        cursor.close()

    except pymysql.Error as err:
        msg = "Failed init database: {}".format(err)
        logger.error(msg)
    finally:
        cnx.close()

    return


def get_jobs(user_id, job_id):

    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()
        query_all = "SELECT job_id, status, original_image_url, filter_id, result_image_url FROM jobs WHERE user_id = %s"
        query_one = "SELECT job_id, status, original_image_url, filter_id, result_image_url FROM jobs WHERE user_id = %s AND job_id = %s"
        query = query_all if job_id is None else query_one
        query_data = user_id if job_id is None else (user_id, job_id)
        cursor.execute(query, query_data)
        results = cursor.fetchall()
        jobs = []
        for row in results:
            job = {
                TAG_JOB_ID: row[0],
                TAG_STATUS: row[1],
                TAG_ORIGINAL_IMAGE_URL: row[2],
                TAG_FILTER_ID: row[3]
            }
            jobs.append(job)
        cursor.close()

        return jobs

    except pymysql.Error as err:
        msg = "Failed get jobs: {0}".format(err)
        logger.error(msg)
        raise


def add_job(job_data):
    user_id = '1111'
    job_id = str(uuid.uuid4())
    job_data['jobId'] = job_id
    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()
        query = "INSERT INTO jobs (user_id, job_id, status, original_image_url, filter_id)" \
                "VALUES (%s, %s, %s, %s, %s)"
        query_data = (user_id, job_id, "IN_PROCESS", job_data[TAG_ORIGINAL_IMAGE_URL],
                      job_data[TAG_FILTER_ID])
        cursor.execute(query, query_data)
        cnx.commit()
        cursor.close()
    except pymysql.Error as err:
        msg = "Failed to insert job: {0}".format(err)
        logger.error(msg)
        raise

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    # Creates the queue
    # channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=json.dumps(job_data),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

    return job_data


def update_job(job_data):
    user_id = '1111'
    job_id = job_data['jobId']
    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()
        query = "UPDATE jobs SET status = %s, original_image_url = %s WHERE user_id = %s AND job_id = %s"
        query_data = (job_data[TAG_STATUS], job_data[TAG_RESULT_IMAGE_URL], user_id, job_id)
        cursor.execute(query, query_data)
        cnx.commit()
        cursor.close()
    except pymysql.Error as err:
        msg = "Failed to insert job: {0}".format(err)
        logger.error(msg)
        raise

    return job_data


@app.route('/test', method='GET')
def handler_get_test():
    logger.info('Processing GET /test')

    data = {
        "status": "OK",
        "message": "TEST OK"
        }
    return data


@app.route('/jobs', method='GET')
@app.route('/jobs/', method='GET')
@app.route('/jobs/<job_id>', method='GET')
def handler_get_jobs(job_id=None):
    logger.info('Processing GET /jobs')

    user_id = '1111'

    try:
        jobs = get_jobs(user_id, job_id)
        res_data = {
            "jobs": jobs
        }
        return res_data
    except Exception as ex:
        msg = ex.message
        error_data = {
            "status": "ERROR",
            "message": msg
        }
        return error_data


@app.route('/jobs', method='POST')
def handler_post_jobs():
    logger.info('Processing POST /jobs')
    data = request.json
    logger.info('body: {0}'.format(data))
    try:
        job = add_job(data)
        data = {
            "status": "OK",
            "message": job
        }
        return data
    except Exception as ex:
        msg = ex.message
        error_data = {
            "status": "ERROR",
            "message": msg
        }
        return error_data


@app.route('/jobs/<job_id>', method='PUT')
def handler_put_job(job_id=None):
    logger.info('Processing PUT /job')
    data = request.json
    logger.info('body: {0}'.format(data))
    try:
        data['jobId'] = job_id
        job = update_job(data)
        data = {
            "status": "OK",
            "message": job
        }
        return data
    except Exception as ex:
        msg = ex.message
        error_data = {
            "status": "ERROR",
            "message": msg
        }
        return error_data


init_db()
logger.info('Starting Image Processor API Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
