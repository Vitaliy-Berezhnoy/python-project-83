import psycopg2
from psycopg2.extras import DictCursor


class UrlsRepo:
    def __init__(self, url_db):
        self.url_db = url_db
#        self.conn = psycopg2.connect(url_db)

    def get_all_urls(self):
        with psycopg2.connect(
                self.url_db).cursor(cursor_factory=DictCursor) as cur:
            query = """
            SELECT
                urls.id,
                urls.name,
                MAX(url_checks.created_at) AS date_last_check,
                (
                SELECT url_checks.status_code
                FROM url_checks
                WHERE url_checks.url_id = urls.id
                ORDER BY url_checks.created_at DESC
                LIMIT 1
                ) AS status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, urls.name
            ORDER BY urls.id DESC;
            """
            cur.execute(query)
            urls = cur.fetchall()
        return urls

    def add_url(self, url):
        conn = psycopg2.connect(self.url_db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
                (url,)
            )
            url_id = cur.fetchone()
            conn.commit()
        conn.close()
        return url_id['id']

    def find_same_url(self, url):
        with psycopg2.connect(
                self.url_db).cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT id FROM urls WHERE name = (%s);', (url,))
            url_id = cur.fetchone()
        return url_id['id'] if url_id else None

    def get_url(self, url_id):
        with psycopg2.connect(
                self.url_db).cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            result = cur.fetchone()
        return result

    def add_check(self, check):
        conn = psycopg2.connect(self.url_db)
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query = """
            INSERT INTO url_checks  (
                url_id,
                status_code,
                h1,
                title,
                description
            )
            VALUES (
                %(url_id)s,
                %(status_code)s,
                %(h1)s,
                %(title)s,
                %(description)s
            )
            RETURNING id;
            """
            cur.execute(query, check)
            check_id = cur.fetchone()
            conn.commit()
        conn.close()
        return check_id['id']

    def get_url_checks(self, url_id):
        with psycopg2.connect(
                self.url_db).cursor(cursor_factory=DictCursor) as cur:
            query = 'SELECT * FROM url_checks WHERE url_id = %s;'
            cur.execute(query, (url_id,))
            url_checks = cur.fetchall()
        return url_checks
