from store import save_data, load_data
from commands import (
    hello,
    exit_program,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    get_upcoming_birthdays,
)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")

    commands = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": get_upcoming_birthdays,
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
