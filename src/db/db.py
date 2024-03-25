import sqlite3

class BDController():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user (tg_id INTEGER, username TEXT, domen TEXT, time INTEGER)")
        self.conn.commit()
    
    def check(self, id):
        self.cur.execute("SELECT * FROM user WHERE tg_id == ?", (id,))
        if self.cur.fetchall():
            return True
        else:
            return False
    def add_user(self, tg_id, username, domen, time):
        self.cur.execute("INSERT INTO user (tg_id, username, domen, time) VALUES(?, ?, ?, ?)", (tg_id, username, domen, time))
        self.conn.commit()
        
    def get_data(self, tg_id):
        self.cur.execute(f"SELECT domen, time FROM user WHERE tg_id = {tg_id}")
        return "\n".join([" ".join(map(str, item)) for item in self.cur.fetchall()])
    def delete_data(self, tg_id):
        self.cur.execute(f"DELETE FROM user WHERE tg_id = {tg_id}")
        self.conn.commit()




