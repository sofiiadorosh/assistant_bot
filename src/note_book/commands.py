from src.exceptions import ArgumentInvalidError
from src.note_book.models import Note
from src.decorators import input_error, persist_data


@input_error
@persist_data
def add_note(args, note_book):
    if not args:
        raise ArgumentInvalidError
    title = args[0]
    content = " ".join(args[1:])

    note = note_book.find_note(title)
    if note is None:
        note = Note(title, content)
        note_book.add_note(note)
        return f"Note '{title}' added."

    note.content = content
    return f"Note '{title}' updated."


@input_error
def all_notes(args, note_book):
    return "\n".join(str(note) for note in note_book.values())


@input_error
def find_note(args, note_book):
    try:
        keyword = args[0]
    except ValueError:
        raise ArgumentInvalidError

    notes = note_book.search_notes(keyword)
    return "\n".join(str(note) for note in notes)


@input_error
@persist_data
def change_note(args, note_book):
    if not args:
        raise ArgumentInvalidError
    title = args[0]
    content = " ".join(args[1:])

    note = note_book.find_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.content = content
    return f"Note '{title}' updated."


@input_error
@persist_data
def delete_note(args, note_book):
    try:
        title = args[0]
    except ValueError:
        raise ArgumentInvalidError

    note_book.delete_note(title)
    return f"Note '{title}' deleted."


@input_error
@persist_data
def add_tag(args, note_book):
    try:
        title, tag = args
    except ValueError:
        raise ArgumentInvalidError

    note = note_book.find_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.add_tag(tag)
    return f"Tag '{tag}' added to note '{title}'."


@input_error
def find_notes(args, note_book):
    try:
        tag = args[0]
    except ValueError:
        raise ArgumentInvalidError

    notes = note_book.find_notes(tag)
    return "\n".join(str(note) for note in notes)


@input_error
def all_tags(args, note_book):
    return ", ".join(note_book.all_tags())