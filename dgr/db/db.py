import psycopg2

from ..config import Config


class DB:
    def __init__(self, config:Config) -> None:
        self.conn = psycopg2.connect(
            host = config.db.host,
            port = config.db.port,
            user = config.db.user,
            passowrd = config.db.passowrd,
            dbname = config.db.dbname,
        )
    def querymany(self, q, params):
        # use %s without quotes for parameters
        with self.conn.cursor() as cur:
            cur.execute(q, params)
            return cur.fetchall()
    def queryone(self, q, params):
        # use %s without quotes for parameters
        with self.conn.cursor() as cur:
            cur.execute(q, params)
            return cur.fetchone()
    def execute(self, s, params):
        # use %s without quotes for parameters
        with self.conn.cursor() as cur:
            cur.execute(s, params)
    def executefetch(self, s, params):
        # use %s without quotes for parameters
        with self.conn.cursor() as cur:
            cur.execute(s, params)
            r = cur.fetchall()
            cur.execute("commit;")
            return r


