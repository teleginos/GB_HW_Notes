import sqlite3


class Database:

    def __init__(self, db_name="notes.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
        """)
        self.connection.commit()

    def insert(self, title, content):
        self.cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        self.connection.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT id, title FROM notes")
        return self.cursor.fetchall()

    def fetch_one(self, note_id):
        self.cursor.execute("SELECT title, content FROM notes WHERE id=?", (note_id,))
        return self.cursor.fetchone()

    def update(self, note_id, title=None, content=None):
        if title and content:
            self.cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content,
                                                                                   note_id))
        elif title:
            self.cursor.execute("UPDATE notes SET title=? WHERE id=?", (title, note_id))
        elif content:
            self.cursor.execute("UPDATE notes SET content=? WHERE id=?", (content, note_id))
        self.connection.commit()

    def delete(self, note_id):
        self.cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()
