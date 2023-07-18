"""Database session

This module contains utilities for connecting to PosgreSQL database.
Expired: October 16, 2023

"""
import time
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

from .log import get_log
from config import settings


log = get_log(__name__)


def get_db():
    while True:
        try:
            conn = psycopg2.connect(
                settings.CONNECTION, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            log.info(f"🏢 Connected to {conn.info.dbname}")
            break
        except Exception as error:
            print("Connecting to database failed")
            print("Error: ", error)
            time.sleep(2)
    return conn, cursor


class Database():
    def __init__(self) -> None:
        self.conn, self.cur = get_db()
        self.pwd = settings.PWD

    def commit(self):
        self.conn.commit()

    def __verify(self):
        """Admin authentication

        For executing DDL commands
        """
        pwd = input("Enter password: ")
        return pwd == self.pwd

    def close(self):
        self.commit()
        self.conn.close()

    def execute(self, command, *values):
        try:
            self.cur.execute(command, tuple(values))
        except Exception as e:
            log.warning(f"💡 Error: {e}")

    def record(self, command: str, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchone()

    def records(self, command, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchall()

    # TODO: LOAD
    def add_summoner(self, puuid: str, name: str, region: str):
        if not self.__verify():
            log.warning("💡 Only admin can execute this command")
            return

        query = self.record("SELECT * FROM summoners where s_id = (%s)", puuid)
        if not query:
            url = f"https://www.op.gg/summoners/vn/{name.replace(' ', '%20')}"
            self.execute("INSERT INTO summoners VALUES (%s, %s, %s, %s)",
                         puuid, name, region, url)
            self.commit()
        else:
            log.warning("💡 Summoner already existed")


if __name__ == "__main__":
    db = Database()

    db.add_summoner("nini2innn", "Cozy Bearrrrr", "vn2")

    data = db.records("select * from summoners")

    df = pd.DataFrame([i.copy() for i in data])
    print(df)
