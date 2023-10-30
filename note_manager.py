from database import Database


class NoteManager:
    def __init__(self, database):
        self.db = database

    def create(self, title, content):
        self.db.insert(title, content)

    def list(self):
        for row in self.db.fetch_all():
            print(f"{row[0]}. {row[1]}")

    def view(self, note_id):
        note = self.db.fetch_one(note_id)
        if note:
            print(f"Title: {note[0]}\nContent: {note[1]}")
        else:
            print(f"Note not found")

    def edit(self, note_id, title=None, content=None):
        self.db.update(note_id, title, content)

    def delete(self, note_id):
        self.db.delete(note_id)
