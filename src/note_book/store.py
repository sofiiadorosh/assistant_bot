import json

from src.note_book.models import NoteBook, Note


FILENAME = "samples/notes.json"


def save_data(book, filename=FILENAME):
    notes = {}
    for title, note in book.data.items():
        notes[title] = {
            "title": note.title.value,
            "content": note.content.value,
            "tags": list(note.tags),
        }
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(notes, fh, indent=2, ensure_ascii=False)


def load_data(filename=FILENAME):
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            notes = json.load(fh)
    except FileNotFoundError:
        return NoteBook()

    book = NoteBook()
    for title, saved_note in notes.items():
        note = Note(saved_note["title"], saved_note["content"])
        for tag in saved_note.get("tags", []):
            note.add_tag(tag)
        book.add_note(note)
    return book
