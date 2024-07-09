import psycopg2
from psycopg2.extras import NamedTupleCursor
from contextlib import contextmanager
from dotenv import load_dotenv
from .log import LOGGER
import datetime
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
            "SELECT * FROM urls ORDER BY created_at DESC;",
        )
        urls = cur.fetchall()
        return urls


def get_url(id):
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            'SELECT * FROM urls WHERE id = %s", (id,)',
        )
        url_data = cur.fetchone()
        if not url_data:
            return "URL not found", 404
        return url_data


def add_url(url):
    with connectionDB() as conn, \
         conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "INSERT INTO urls (name, created_at) \
            VALUES (%s, %s);",
            (url, datetime.now()),
        )
        id = cur.fetchone().id
        conn.commit()
        return id
