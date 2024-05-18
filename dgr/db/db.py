import psycopg2


class DB:
    def __init__(self, config) -> None:
        self.conn = psycopg2.connect(**config.db.params)
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

