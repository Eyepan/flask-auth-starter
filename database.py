import sqlite3
import bcrypt


class DB:
    def __init__(self):
        self.query(
            "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
        self.query("CREATE TABLE IF NOT EXISTS salt(salt TEXT)")
        sv = self.query("SELECT * FROM salt")
        if sv:
            self.salt = sv[0][0]
        else:
            self.create_salt()
            self.salt = self.query("SELECT * FROM salt")[0][0]

    def create_salt(self):
        salt = bcrypt.gensalt()
        self.query("INSERT INTO salt VALUES(?)", (salt,))

    def get_salt(self):
        return self.salt

    def connection(self):
        return sqlite3.connect("database.db")

    def query(self, query, args=()):
        print("QUERY:", query)
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            rv = cursor.fetchall()
            cursor.close()
        return rv


db = DB()
