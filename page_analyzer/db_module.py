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
        curs.execute(query, (url.get('url'),))
        id = curs.fetchone()['id']
        conn.commit()
        return id


def get_url(conn, id):
    query = 'SELECT * FROM urls WHERE id = %s'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query, (id,))
        url_info = curs.fetchone()
        if not url_info:
            return None
        return url_info


def show_urls(conn):
    query = 'SELECT * FROM urls ORDER BY id DESC'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query)
        urls_all = curs.fetchall()
        return urls_all


def url_unique_id(conn, url):
    query = 'SELECT id, name FROM urls WHERE name = %s'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query, (url['url'],))
        url_id = curs.fetchone()
        if not url_id:
            return None
        return url_id['id']
