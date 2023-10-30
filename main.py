import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QListWidget, \
    QLineEdit

from database import Database
from note_manager import NoteManager


class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.manager = NoteManager(self.db)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Notes App')

        # Widgets
        self.notes_list = QListWidget()
        self.text_title = QLineEdit('Title')
        self.text_content = QTextEdit('Content')
        self.btn_add = QPushButton('Add Note')
        self.btn_edit = QPushButton('Edit Note')
        self.btn_delete = QPushButton('Delete Note')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.notes_list)
        layout.addWidget(self.text_title)
        layout.addWidget(self.text_content)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect signals
        self.btn_add.clicked.connect(self.add_note)
        self.btn_edit.clicked.connect(self.edit_note)
        self.btn_delete.clicked.connect(self.delete_note)
        self.notes_list.itemClicked.connect(self.display_note)

        # Load notes
        self.load_notes()

    def load_notes(self):
        self.notes_list.clear()
        notes = self.manager.db.fetch_all()
        for note in notes:
            self.notes_list.addItem(f"{note[0]}. {note[1]}")

    def add_note(self):
        title = self.text_title.text()
        content = self.text_content.toPlainText()
        self.manager.create(title, content)
        self.load_notes()

    def edit_note(self):
        current_item = self.notes_list.currentItem()
        if current_item:
            note_id = int(current_item.text().split('.')[0])
            title = self.text_title.text()
            content = self.text_content.toPlainText()
            self.manager.edit(note_id, title, content)
            self.load_notes()

    def delete_note(self):
        current_item = self.notes_list.currentItem()
        if current_item:
            note_id = int(current_item.text().split('.')[0])
            self.manager.delete(note_id)
            self.load_notes()

    def display_note(self, item):
        note_id = int(item.text().split('.')[0])
        note = self.manager.db.fetch_one(note_id)
        self.text_title.setText(note[0])
        self.text_content.setText(note[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = NotesApp()
    main_win.show()
    sys.exit(app.exec_())
