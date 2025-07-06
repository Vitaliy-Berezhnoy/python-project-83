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




#def get_all_urls()