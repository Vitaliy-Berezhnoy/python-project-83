import psycopg2
from psycopg2.extras import DictCursor


class UrlsRepo:
    def __init__(self, url_db):
        self.conn = psycopg2.connect(url_db)

    def get_all_urls(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls ORDER BY urls.id DESC;')
            urls = cur.fetchall()
        return urls

    def add_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
                (url,)
            )
            url_id = cur.fetchone()
            self.conn.commit()
            return url_id['id']

    def find_same_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT id FROM urls WHERE name = (%s)', (url,))
            url_id = cur.fetchone()
        return url_id

    def get_url(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            result = cur.fetchone()
        return result
