from src.store import save_data, load_data
from src.commands import (
    hello,
    exit_program,
    show_help,
    add_contact,
    change_contact,
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


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")
    print(show_help([], contacts))

    commands = {
        "hello": hello,
        "help": show_help,
        "add-contact": add_contact,
        "change-contact": change_contact,
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
        "close": exit_program,
        "exit": exit_program,
    }

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)
        action = commands.get(command.lower())

        if action:
            result = action(args, contacts)
            if result == "exit":
                save_data(contacts)
                print("Goodbye!")
                break
            if result:
                print(result)
        else:
            print("Invalid command.")
