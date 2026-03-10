from src.exceptions import ArgumentInvalidError
from src.note_book.models import Note, Content
from src.decorators import input_error, persist_data


@input_error
@persist_data
def add_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.find_note_by_title(title)
    if note is None:
        note = Note(title, content)
        notes.add_note(note)
        return f"Note '{title}' added."

    note.content = Content(content)
    return f"Note '{title}' updated."


@input_error
def all_notes(args, notes):
    if not notes.values():
        return "No notes yet."
    return "\n".join(str(note) for note in notes.values())


@input_error
def find_note_by_keyword(args, notes):
    try:
        (keyword,) = args
    except ValueError:
        raise ArgumentInvalidError

    found_notes = notes.find_note_by_keyword(keyword)
    if not found_notes:
        return f"No notes found with keyword '{keyword}'."
    return "\n".join(str(note) for note in found_notes)


@input_error
@persist_data
def edit_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.find_note_by_title(title)
    if note is None:
        return f"Note '{title}' not found."

    note.content = Content(content)
    return f"Note '{title}' updated."


@input_error
@persist_data
def delete_note(args, notes):
    try:
        (title,) = args
    except ValueError:
        raise ArgumentInvalidError

    notes.delete_note(title)
    return f"Note '{title}' deleted."


@input_error
@persist_data
def add_tag(args, notes):
    try:
        title, tag = args
    except ValueError:
        raise ArgumentInvalidError

    note = notes.find_note_by_title(title)
    if note is None:
        return f"Note '{title}' not found."

    note.add_tag(tag)
    return f"Note '{title}' updated."


@input_error
def find_notes_by_tag(args, notes):
    try:
        (tag,) = args
    except ValueError:
        raise ArgumentInvalidError

    found_notes = notes.find_note_by_tag(tag)
    if not found_notes:
        return f"No notes found with tag '{tag}'."
    return "\n".join(str(note) for note in found_notes)


@input_error
def all_tags(args, notes):
    if not notes.all_tags():
        return "No tags yet."
    return ", ".join(notes.all_tags())