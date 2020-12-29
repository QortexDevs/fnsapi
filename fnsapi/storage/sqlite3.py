import sqlite3
import datetime

class Storage:

    def __init__(self):
        self.connection = sqlite3.connect('storage.db')
        self.cursor = connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS fns_api_session_tokens (token TEXT NOT NULL, expire_time TIMESTAMP)')
    
    def delete_outdated_tokens(self):
        cursor = self.cursor
        cursor.execute('DELETE FROM fns_api_session_tokens WHERE expire_time < ?', datetime.datetime('now'))

    def get_stored_token(self):
        cursor = self.cursor
        self.delete_outdated_tokens()
        cursor.execute('SELECT * FROM fns_api_session_tokens ORDER BY expire_time DESC')
        rows = cursor.fetchall()
        if (len(rows) <= 0):
            return None
        return rows[0].token
    
    def store_token(self, token, expire_time):
        cursor = self.cursor
        cursor.execute('INSERT INTO fns_api_session_tokens (token, expire_time) VALUES(?, ?)', (token, expire_time))