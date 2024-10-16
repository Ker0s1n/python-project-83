import psycopg2
from psycopg2.extras import RealDictCursor


def connect_db(DATABASE_URL):
    try:
        return psycopg2.connect(DATABASE_URL)
    except ConnectionError:
        print('Can`t establish connection to database')


def close(conn):
    conn.close()


def add_url(conn, url):
    query = '''
    INSERT INTO urls (name) VALUES (%s)
    RETURNING id
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query, (url.get('url_adress'),))
        id = curs.fetchone()['id']
        conn.commit()
        return id
