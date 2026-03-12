from assistant_bot.exceptions import ArgumentInvalidError
from assistant_bot.note_book.models import Note
from assistant_bot.decorators import input_error, persist_data


@input_error
@persist_data
def add_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.get_note(title)
    if note is None:
        note = Note(title, content)
        notes.add_note(note)
        return f"Note '{title}' added."

    note.edit_content(content)
    return f"Note '{title}' updated."


@input_error
def all_notes(args, notes):
    if not notes.values():
        return "No notes yet."
    return "\n".join(str(note) for note in notes.values())


@input_error
def find_notes(args, notes):
    try:
        if not args:
            raise ValueError
        field, *rest = ("keyword", *args) if len(args) == 1 else args
        if not rest:
            raise ValueError
        value = " ".join(rest).strip()
        if not value:
            raise ValueError
        field = field.lower()
        if field not in ("keyword", "tag"):
            raise ValueError
    except ValueError:
        raise ArgumentInvalidError
    found_notes = notes.find_note(field, value)
    if not found_notes:
        return f"No notes found with {field} '{value}'."
    return "\n".join(str(note) for note in found_notes)


@input_error
@persist_data
def edit_note(args, notes):
    try:
        title, *rest = args
        content = " ".join(rest)
    except ValueError:
        raise ArgumentInvalidError

    note = notes.get_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.edit_content(content)
    return f"Note '{title}' updated."


@input_error
@persist_data
def delete_note(args, notes):
    try:
        (title,) = args
    except ValueError:
        raise ArgumentInvalidError

    note = notes.get_note(title)
    if note is None:
        return f"Note '{title}' not found."

    notes.delete_note(note.title.value)
    return f"Note '{title}' deleted."


@input_error
@persist_data
def add_tag(args, notes):
    try:
        title, tag = args
    except ValueError:
        raise ArgumentInvalidError

    note = notes.get_note(title)
    if note is None:
        return f"Note '{title}' not found."

    note.add_tag(tag)
    return f"Note '{title}' updated."


@input_error
def all_tags(args, notes):
    if not notes.all_tags():
        return "No tags yet."
    return ", ".join(notes.all_tags())


@input_error
def sort_notes(args, notes):
    if not notes.data:
        return "No notes yet."
    return "\n".join(str(note) for note in notes.sort_notes_by_title())