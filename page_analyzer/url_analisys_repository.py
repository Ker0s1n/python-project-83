from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
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
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            urls_all = cur.fetchall()
            return urls_all

    def find(self, id):
        query = 'SELECT * FROM urls WHERE id = %s'
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            url_info = cur.fetchone()
        if not url_info:
            return None
        return url_info

    def get_id(self, url):
        query = 'SELECT id, name FROM urls WHERE name = %s'
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (url,))
            url_id = cur.fetchone()
            if not url_id:
                return None
            return url_id['id']

    def add(self, url):
        query = '''
        INSERT INTO urls (name) VALUES (%s)
        RETURNING id
        '''
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (url,))
            id = cur.fetchone()['id']
            self.conn.commit()
            return id

    def check(self, url_check, status_code, analysis):
        query = '''
        INSERT INTO url_cheks (
        url_id, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s)
        '''
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                query,
                (
                    url_check.get('id'),
                    status_code,
                    analysis.get('h1'),
                    analysis.get('title'),
                    analysis.get('description')
                )
            )
            self.conn.commit()
            return url_check.get('id')

    def get_checks(self, id):
        query = 'SELECT * FROM url_cheks WHERE url_id = %s ORDER BY id DESC'
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id,))
            url_checks_all = cur.fetchall()
            return url_checks_all
