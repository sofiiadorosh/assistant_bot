import json
from pathlib import Path

from src.note_book.models import NoteBook, Note, NoteBookError


_BASE_DIR = Path(__file__).resolve().parent.parent.parent
FILENAME = _BASE_DIR / "samples" / "notes.json"


def save_data(book, filename=FILENAME):
    notes = {}
    for title, note in book.data.items():
        notes[title] = {
            "title": note.title.value,
            "content": note.content.value,
            "tags": list(note.tags),
        }
    with open(Path(filename), "w", encoding="utf-8") as fh:
        json.dump(notes, fh, indent=2, ensure_ascii=False)


def load_data(filename=FILENAME):
    try:
        with open(Path(filename), "r", encoding="utf-8") as fh:
            notes = json.load(fh)
    except FileNotFoundError:
        return NoteBook()
    except json.JSONDecodeError:
        return NoteBook()

    book = NoteBook()
    for title, saved_note in notes.items():
        if not isinstance(saved_note, dict) or "title" not in saved_note or "content" not in saved_note:
            continue
        try:
            note = Note(saved_note["title"], saved_note["content"])
            for tag in saved_note.get("tags", []):
                note.add_tag(tag)
            book.add_note(note)
        except (TypeError, ValueError, KeyError, NoteBookError):
            continue
    return book
