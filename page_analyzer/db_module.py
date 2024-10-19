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
        curs.execute(query, (url,))
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
    query = '''
    WITH last_check AS (
        SELECT DISTINCT ON (url_id)
            url_id,
            created_at,
            status_code
        FROM url_cheks
        ORDER BY url_id, created_at DESC
    )
    SELECT
        urls.id,
        urls.name,
        last_check.created_at as check,
        last_check.status_code as status
    FROM urls
    LEFT JOIN last_check
    ON urls.id = last_check.url_id
    ORDER BY urls.id
    DESC
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query)
        urls_all = curs.fetchall()
        return urls_all


def url_unique_id(conn, url):
    query = 'SELECT id, name FROM urls WHERE name = %s'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query, (url,))
        url_id = curs.fetchone()
        if not url_id:
            return None
        return url_id['id']


def add_url_check(conn, url_check, status_code, analysis):
    query = '''
    INSERT INTO url_cheks (
    url_id, status_code, h1, title, description)
    VALUES (%s, %s, %s, %s, %s)
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(
            query,
            (
                url_check.get('id'),
                status_code,
                analysis.get('h1'),
                analysis.get('title'),
                analysis.get('description')
            )
        )
        conn.commit()
        return url_check.get('id')


def show_url_checks(conn, id):
    query = 'SELECT * FROM url_cheks WHERE url_id = %s ORDER BY id DESC'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(query, (id,))
        url_checks_all = curs.fetchall()
        return url_checks_all
