from src.address_book.store import load_data as load_address_book
from src.note_book.store import load_data as load_note_book
from src.commands import (
    hello,
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
)
from src.note_book.commands import (
    add_note,
    all_notes,
    find_note_by_keyword,
    edit_note,
    delete_note,
    add_tag,
    find_notes_by_tag,
    all_tags,
)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    contacts = load_address_book()
    notes = load_note_book()
    print("Welcome to the assistant bot!")
    print(show_help([], contacts, notes))

    common_commands = {
        "hello": hello,
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
        "delete-contact": delete_contact,
    }

    notes_commands = {
        "add-note": add_note,
        "all-notes": all_notes,
        "find-note": find_note_by_keyword,
        "edit-note": edit_note,
        "delete-note": delete_note,
        "add-tag": add_tag,
        "find-notes": find_notes_by_tag,
        "all-tags": all_tags,
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
            print("Invalid command.")
