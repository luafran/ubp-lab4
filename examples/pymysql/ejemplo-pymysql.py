import pymysql

mysql_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '123456',
    'db': 'spi'
}

def insert_test():
    print 'insert test...'
    try:
        cnx = pymysql.connect(**mysql_config)
        cursor = cnx.cursor()
        
        query = 'INSERT INTO test (id, msg) VALUES (%s, %s)'
        data = ('200', 'mensaje2')
        cursor.execute(query, data)
        cnx.commit()
        print 'executed'
        cursor.close()

    except pymysql.Error as err:
        msg = "Insert failed: {}".format(err)
        print msg
    finally:
        cnx.close()

    return

if __name__ == '__main__':
    insert_test()

