import logging
import os
import pymysql
from bottle import Bottle, run, request, response
import Crypto.PublicKey.RSA as RSA
import python_jwt as jwt
import jws

LISTEN_PORT = 8082


logger = logging.getLogger('jobs-frontend-svc')
logger.setLevel(logging.DEBUG)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

public_key_file = os.path.join(os.path.dirname(__file__), 'keypair.pub')
with open(public_key_file, 'r') as fd:
    public_key = RSA.importKey(fd.read())

mysql_config = {
    'host': os.environ['MYSQL_ENDPOINT'],
    'user': os.environ['MYSQL_USER'],
    'passwd': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE']
}

app = Bottle()


def init_db():
    logger.info('Processing init database')

    cnx = None
    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()

        create_table = "create table if not exists spt.jobs(userId varchar(50)," \
                       "text varchar(50)," \
                       "duration integer," \
                       "count integer)"
        cursor.execute(create_table)
        cursor.close()

    except pymysql.Error as err:
        msg = "Failed init database: {}".format(err)
        logger.error(msg)
    finally:
        if cnx:
            cnx.close()

    return


def db_get_jobs(user_id):

    return ret_data


@app.route('/test', method='GET')
def get_test():
    logger.info('Processing GET /test')
    logger.debug('Authorization: {}'.format(request.headers['Authorization']))
    ret_data = {
        "status": "OK"
    }
    return ret_data


@app.route('/jobs', method='GET')
def get_jobs():
    logger.info('Processing GET /jobs')

    try:
        token_type, token = request.headers.get('Authorization').split()
        logger.debug('token_type: {}, token: {}'.format(token_type, token))
        header, claims = jwt.verify_jwt(token, public_key, ['RS256'])
    except (jws.exceptions.SignatureError, ValueError) as ex:
        message = "Invalid token: {}".format(ex)
        logger.warn(message)
        response.status = 401
        ret_data = {
            "message": message
        }
        return ret_data

    user_id = claims['userId']

    jobs = []
    cnx = None
    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()
        select_user = "SELECT text, duration, count FROM jobs WHERE userId = %s"
        data_user = user_id
        cursor.execute(select_user, data_user)
        results = cursor.fetchall()

        for row in results:
            logger.debug(row)
        cursor.close()

        ret_data = {
            'jobs': jobs
        }
    except pymysql.Error as err:
        message = "Failed to select jobs: {}".format(err)
        logger.error(message)
        response.status = 500
        ret_data = {
            "message": message
        }
    finally:
        if cnx:
            cnx.close()

    return ret_data


@app.route('/jobs', method='POST')
def post_jobs():
    logger.info('Processing POST /jobs')
    data = request.json
    logger.info(data)

    token_type, token = request.headers['Authorization'].split()
    logger.debug('token_type: {}, token: '.format(token_type, token))

    return {}


'''
RUN APP
'''

init_db()
logger.info('Starting Authentication Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
