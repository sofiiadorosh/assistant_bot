import json
from pathlib import Path

from assistant_bot.address_book.models import AddressBook, Record, AddressBookError
from assistant_bot.note_book.models import NoteBook, Note, NoteBookError
from assistant_bot.address_book.store import save_data as save_address_book
from assistant_bot.note_book.store import save_data as save_note_book


_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"
FILENAME_CONTACTS = _SAMPLES_DIR / "contacts.json"
FILENAME_NOTES = _SAMPLES_DIR / "notes.json"


def load_sample(contacts, notes):
    address_book = load_contacts()
    note_book = load_notes()
    save_address_book(address_book)
    save_note_book(note_book)
    contacts.add_records(address_book.data.values())
    notes.add_notes(note_book.data.values())


def load_contacts(filename=FILENAME_CONTACTS):
    try:
        with open(Path(filename), "r", encoding="utf-8") as fh:
            contacts = json.load(fh)
    except FileNotFoundError:
        return AddressBook()
    except json.JSONDecodeError:
        return AddressBook()

    book = AddressBook()
    for name, contact in contacts.items():
        if not isinstance(contact, dict) or "name" not in contact:
            continue
        try:
            record = Record(contact["name"])
            for phone in contact.get("phones", []):
                record.add_phone(str(phone))
            if contact.get("birthday"):
                record.set_birthday(contact["birthday"])
            if contact.get("email"):
                record.set_email(contact["email"])
            if contact.get("address"):
                record.set_address(contact["address"])
            book.add_record(record)
        except (TypeError, ValueError, KeyError, AddressBookError):
            continue
    return book


def load_notes(filename=FILENAME_NOTES):
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