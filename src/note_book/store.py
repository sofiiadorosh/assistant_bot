from pathlib import Path
from pickle import dump, load

from src.note_book.models import NoteBook


_DATA_DIR = Path.home() / ".assistant_bot"
_DATA_DIR.mkdir(exist_ok=True)
FILENAME = _DATA_DIR / "note_book.pkl"


def save_data(book, filename=FILENAME):
    with open(filename, "wb") as fh:
        dump(book, fh)


def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as fh:
            return load(fh)
    except FileNotFoundError:
        return NoteBook()