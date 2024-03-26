import sqlite3

class BDController():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user (tg_id INTEGER, username TEXT, domen TEXT, time INTEGER, job_id TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS url (domen TEXT, url_id TEXT)")
        self.conn.commit()
    
    def check(self, id):
        self.cur.execute("SELECT * FROM user WHERE tg_id == ?", (id,))
        if self.cur.fetchall():
            return True
        else:
            return False
    def add_user(self, tg_id, username, domen, time, job_id):
        self.cur.execute("INSERT INTO user (tg_id, username, domen, time, job_id) VALUES(?, ?, ?, ?, ?)", (tg_id, username, domen, time, job_id))
        self.conn.commit()
        
    def check_url(self, domen):
        self.cur.execute("SELECT url_id FROM url WHERE domen = ?", (domen,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        
    def add_url(self, domen, url_id):
        if not self.check_url(domen):
            self.cur.execute("INSERT INTO url (domen, url_id) VALUES(?, ?)", (domen, url_id))
            self.conn.commit()
        
    def get_data(self, tg_id):
        self.cur.execute(f"SELECT domen, time FROM user WHERE tg_id = {tg_id}")
        return "🗂️\n".join([" ".join(map(str, item)) for item in self.cur.fetchall()])
    
    def delete_data(self, tg_id):
        self.cur.execute(f"DELETE FROM user WHERE tg_id = ?", (tg_id,))
        self.conn.commit()
    
    def delete_job(self, job_id):
        self.cur.execute(f"DELETE FROM user WHERE job_id= ?", (job_id,))
        self.conn.commit()
        
    def get_button_data(self, tg_id):
        self.cur.execute("SELECT domen, job_id FROM user WHERE tg_id = ?", (tg_id,))
        result = self.cur.fetchall()
        if result:
            return result







