from src.address_book.store import load_data as load_address_book
from src.note_book.store import load_data as load_note_book
from src.commands import (
    hello,
    sample,
    exit_program,
    show_help,
)
from src.address_book.commands import (
    add_contact,
    edit_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    get_upcoming_birthdays,
    add_email,
    edit_email,
    add_address,
    edit_address,
    delete_contact,
    find_contact,
)
from src.note_book.commands import (
    add_note,
    all_notes,
    find_notes,
    edit_note,
    delete_note,
    add_tag,
    all_tags,
    sort_notes,
)
from src.suggest_command import suggest_command


SHORT_ACTION = {"a": "add", "e": "edit", "d": "delete", "s": "sort", "sh": "show", "f": "find"}
SHORT_ENTITY = {"c": "contact", "n": "note", "p": "phone", "e": "email", "a": "address", "b": "birthday", "t": "tag"}
ALL_ACTION = {"c": "all-contacts", "n": "all-notes", "t": "all-tags"}
BIRTHDAY_ACTION = {"b": "birthdays"}

SHORT_TO_FULL = {
    ("add", "contact"): "add-contact",
    ("find", "contact"): "find-contact",
    ("delete", "contact"): "delete-contact",
    ("edit", "contact"): "edit-contact",
    ("show", "phone"): "show-phone",
    ("add", "birthday"): "add-birthday",
    ("show", "birthday"): "show-birthday",
    ("add", "email"): "add-email",
    ("edit", "email"): "edit-email",
    ("add", "address"): "add-address",
    ("edit", "address"): "edit-address",
    ("add", "note"): "add-note",
    ("find", "note"): "find-note",
    ("edit", "note"): "edit-note",
    ("delete", "note"): "delete-note",
    ("add", "tag"): "add-tag",
    ("sort", "note"): "sort-notes",
}


def resolve_short_command(command, args):
    full = BIRTHDAY_ACTION.get(command.lower())
    if full:
        return full, args if args else ["7"]
    if not args:
        full = ALL_ACTION.get(command.lower())
        return (full, []) if full else (command, args)

    action = SHORT_ACTION.get(command.lower())
    entity = SHORT_ENTITY.get(args[0].lower())
    if not action or not entity:
        return command, args

    rest = args[1:]
    full = SHORT_TO_FULL.get((action, entity))
    return (full, rest) if full else (command, args)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    cmd, args = resolve_short_command(cmd, args)
    return cmd, *args


def main():
    contacts = load_address_book()
    notes = load_note_book()
    print("Welcome to the assistant bot!")
    print(show_help([], contacts, notes))

    common_commands = {
        "hello": hello,
        "sample": sample,
        "help": show_help,
        "close": exit_program,
        "exit": exit_program,
    }

    contacts_commands = {
        "add-contact": add_contact,
        "edit-contact": edit_contact,
        "show-phone": show_phone,
        "all-contacts": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_upcoming_birthdays,
        "add-email": add_email,
        "edit-email": edit_email,
        "add-address": add_address,
        "edit-address": edit_address,
        "find-contact": find_contact,
        "delete-contact": delete_contact,
    }

    notes_commands = {
        "add-note": add_note,
        "all-notes": all_notes,
        "find-note": find_notes,
        "edit-note": edit_note,
        "delete-note": delete_note,
        "add-tag": add_tag,
        "all-tags": all_tags,
        "sort-notes": sort_notes,
    }

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)
        common_action = common_commands.get(command.lower())
        contacts_action = contacts_commands.get(command.lower())
        notes_action = notes_commands.get(command.lower())

        if common_action:
            result = common_action(args, contacts=contacts, notes=notes)
            if result == "exit":
                print("Goodbye!")
                break
            if result:
                print(result)
        elif contacts_action:
            result = contacts_action(args, contacts=contacts)
            if result:
                print(result)
        elif notes_action:
            result = notes_action(args, notes=notes)
            if result:
                print(result)
        else:
            suggested_cmd, suggestion_message = suggest_command(user_input)
            if suggested_cmd and suggestion_message:
                print(f"Unknown command. {suggestion_message}")
            else:
                print("Unknown command. Type 'help' to see available commands.")
