
from . import SessionStorage
import sqlite3
from openwx.utils import json_loads, json_dumps


__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS wechat_robot(id TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL);
"""
class SQLiteStorage(SessionStorage):
    """


    SQLiteStorage 会把 session 存储在一个 sqlite 数据库中

    seesion_storage = SQLiteStorage

    """

    def __init__(self, filename='db.sqlite3'):
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.db.text_factory = str
        self.db.execute(__CREATE_TABLE_SQL__)
        print("create wechat robot db.")

    def get(self, id):
        session_json = self.db.execute(
            "SELECT value FROM wechat_robot WHERE id=? LIMIT 1;", (id, )
        ).fetchone()
        print("sqlite get {}".format(session_json))
        if session_json is None:
            return {}
        return json_loads(session_json[0])

    def set(self, id, value):
        self.db.execute(
            "INSERT OR REPLACE INTO wechat_robot (id, value) VALUES (?, ?);",
            (id, json_dumps(value))
        )
        print("sqlite set {}".format(value))
        self.db.commit()

    def delete(self, id):
        self.db.execute("DELETE FROM wechat_robot WHERE id=?;", (id, ))
        self.db.commit()


