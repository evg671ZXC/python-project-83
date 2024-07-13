import psycopg2
from psycopg2.extras import NamedTupleCursor
from contextlib import contextmanager
from dotenv import load_dotenv
from .log import LOGGER
from datetime import datetime
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


@contextmanager
def connectionDB():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    except psycopg2.DatabaseError as e:
        LOGGER.error(e)
        raise e
    finally:
        LOGGER.info('Connection opened successfully.')
        conn.close()


def get_urls():
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            '''SELECT * FROM urls ORDER BY id ASC;''',
        )
        urls = cur.fetchall()
        return urls


def get_url(id):
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            '''SELECT * FROM urls WHERE id = %s''', (id,),
        )
        url_data = cur.fetchone()
        if not url_data:
            return "URL not found", 404
        return url_data


def get_urls_checks():
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            '''SELECT DISTINCT ON (url_id) * FROM url_checks ORDER BY url_id DESC, id ASC;'''
            )
        urls_checks = cur.fetchall()
        return urls_checks


def get_url_checks_by_id(url_id):
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            '''SELECT * FROM url_checks WHERE url_id = %s''', (url_id,),
        )
        url_checks_data = cur.fetchone()
        return url_checks_data


def add_url(url):
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            '''INSERT INTO urls (name, created_at) \
            VALUES (%s, %s) RETURNING id;''',
            (url, datetime.today()),
        )
        id = cur.fetchone().id
        conn.commit()
        return id


def add_url_checks(url_id, result_check):
    with connectionDB() as conn, \
         conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)\
            VALUES (%s, %s, %s, %s, %s, %s);''',
            (   
                url_id,
                result_check["status_code"],
                result_check["h1"],
                result_check["title"],
                result_check["description"],
                datetime.today()
                )
        )
        conn.commit()