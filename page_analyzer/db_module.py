import psycopg2
# from psycopg2.extras import RealDictCursor


def connect_db(DATABASE_URL):
    try:
        return psycopg2.connect(DATABASE_URL)
    except ConnectionError:
        print('Can`t establish connection to database')
