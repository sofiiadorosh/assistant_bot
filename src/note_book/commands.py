from src.exceptions import ArgumentInvalidError
from src.note_book.models import Note
from src.decorators import input_error, persist_data


@input_error
@persist_data
def add_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.find_note(title)
    if note is None:
        note = Note(title, content)
        notes.add_note(note)
        return f"Note '{title}' added."

    note.content = content
    return f"Note '{title}' updated."


@input_error
def all_notes(args, notes):
    if not notes.values():
        return "No notes found."
    return "\n".join(str(note) for note in notes.values())


@input_error
def find_note_by_keyword(args, notes):
    try:
        (keyword,) = args
    except ValueError:
        raise ArgumentInvalidError

    found_notes = notes.find_notes_by_keyword(keyword)
    if not notes:
        return f"No notes found with keyword '{keyword}'."
    return "\n".join(str(note) for note in found_notes)


@input_error
@persist_data
def change_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.find_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.content = content
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

    note = notes.find_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.add_tag(tag)
    return f"Tag '{tag}' added to note '{title}'."


@input_error
def find_notes_by_tag(args, notes):
    try:
        (tag,) = args
    except ValueError:
        raise ArgumentInvalidError

    notes = notes.find_notes_by_tag(tag)
    if not notes:
        return f"No notes found with tag '{tag}'."
    return "\n".join(str(note) for note in notes)


@input_error
def all_tags(args, notes):
    if not notes.all_tags():
        return "No tags found."
    return ", ".join(notes.all_tags())