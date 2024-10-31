import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, database_url):
        self.database_url = database_url

    def __enter__(self):
        self.conn = psycopg2.connect(
            self.database_url,
            cursor_factory=RealDictCursor
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()
        else:
            print(f'Exception! Error detected: {value} with {type}')


class UrlRepository:
    def __init__(self, database_url):
        self.db = DatabaseConnection(database_url)

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
        with self.db as db:
            db.cursor.execute(query)
            urls_all = db.cursor.fetchall()
            return urls_all

    def find_id(self, id):
        query = 'SELECT * FROM urls WHERE id = %s'
        with self.db as db:
            db.cursor.execute(query, (id,))
            url_info = db.cursor.fetchone()
            if not url_info:
                return None
            return url_info

    def find_url(self, url):
        query = 'SELECT id, name FROM urls WHERE name = %s'
        with self.db as db:
            db.cursor.execute(query, (url,))
            url_info = db.cursor.fetchone()
            if not url_info:
                return None
            return url_info

    def add_url(self, url):
        query = '''
        INSERT INTO urls (name) VALUES (%s)
        RETURNING id
        '''
        with self.db as db:
            db.cursor.execute(query, (url,))
            id = db.cursor.fetchone()['id']
            db.conn.commit()
            return id

    def check(self, url_check, status_code, analysis):
        query = '''
        INSERT INTO url_cheks (
        url_id, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s)
        '''
        query_result = '''
        SELECT DISTINCT ON (url_id) *
            FROM url_cheks
            WHERE url_id = %s
            ORDER BY url_id, created_at DESC
        '''
        with self.db as db:
            db.cursor.execute(
                query,
                (
                    url_check.get('id'),
                    status_code,
                    analysis.get('h1'),
                    analysis.get('title'),
                    analysis.get('description')
                )
            )
            db.conn.commit()
            db.cursor.execute(query_result, (url_check.get('id'),))
            check_info = db.cursor.fetchone()
            return check_info

    def get_checks(self, id):
        query = 'SELECT * FROM url_cheks WHERE url_id = %s ORDER BY id DESC'
        with self.db as db:
            db.cursor.execute(query, (id,))
            url_checks_all = db.cursor.fetchall()
            return url_checks_all
