from src.models import AddressBook, Record
from src.decorators import input_error
from src.exceptions import ArgumentInvalidError, DaysInvalidError


def hello(args, contacts):
    return "Welcome! Type 'help' to see available commands. How can I help you?"


def exit_program(args, contacts):
    return "exit"


def show_help(args, contacts):
    return """
+-----------------------------------------------+------------------------------------------------+
| Command                                       | Description                                    |
+-----------------------------------------------+------------------------------------------------+
| GENERAL                                                                                        |
+-----------------------------------------------+------------------------------------------------+
| hello                                         | Greet the assistant                            |
| help                                          | Show this help message                         |
| close / exit                                  | Exit the assistant                             |
+-----------------------------------------------+------------------------------------------------+
| CONTACTS                                                                                       |
+-----------------------------------------------+------------------------------------------------+
| add-contact <name> <phone>                    | Add a new contact                              |
| change-contact <name> <old_phone> <new_phone> | Change phone number                            |
| show-phone <name>                             | Show phone number(s)                           |
| all-contacts                                  | Display all contacts                           |
| add-birthday <name> <DD.MM.YYYY>              | Add birthday                                   |
| show-birthday <name>                          | Show birthday                                  |
| birthdays <days>                              | Upcoming birthdays                             |
| add-email <name> <email>                      | Add email to contact                           |
| add-address <name> <address>                  | Add address to contact                         |
| search-contacts <field> <query>               | Search by: name, phone, email, address, all    |
| delete-contact <name>                         | Delete a contact                               |
+-----------------------------------------------+------------------------------------------------+
| NOTES                                                                                          |
+-----------------------------------------------+------------------------------------------------+
| add-note <text>                               | Add a new note                                 |
| all-notes                                     | Display all notes                              |
| find-note <keyword>                           | Search notes by keyword                        |
| change-note <id> <new_text>                   | Edit a note                                    |
| delete-note <id>                              | Delete a note                                  |
| add-tag <note_id> <tag>                       | Add a tag to a note                            |
| find-notes <tag>                              | Find notes by tag                              |
| all-tags                                      | Show all tags                                  |
| sort-notes                                    | Sort notes by tags                             |
+-----------------------------------------------+------------------------------------------------+
"""


@input_error
def add_contact(args, contacts: AddressBook):
    try:
        name, phone = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        record = Record(name)
        contacts.add_record(record)
        record.add_phone(phone)
        return f"Contact '{name}' added."

    record.add_phone(phone)
    return f"Contact '{name}' updated."


@input_error
def change_contact(args, contacts: AddressBook):
    try:
        name, old_phone, new_phone = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add' to create."

    record.edit_phone(old_phone, new_phone)

    return f"Contact '{name}' updated."


@input_error
def show_phone(args, contacts: AddressBook):
    try:
        name, = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add' to create."

    return "; ".join(str(phone) for phone in record.phones)


def show_all(args, contacts: AddressBook):
    if not contacts:
        return "No contacts yet. Use 'add' to create."

    return "\n".join(str(record) for record in contacts.values())


@input_error
def add_birthday(args, contacts: AddressBook):
    try:
        name, birthday = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add' to create."

    record.add_birthday(birthday)
    return f"Contact '{name}' updated."


@input_error
def show_birthday(args, contacts: AddressBook):
    try:
        name, = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add' to create."

    if not record.birthday:
        return f"Birthday for '{name}' is not set."

    return str(record.birthday)


@input_error
def get_upcoming_birthdays(args, contacts: AddressBook):
    if not args:
        raise ArgumentInvalidError

    days, = args

    try:
        days = int(days)
        if days < 0:
            raise ValueError
    except ValueError:
        raise DaysInvalidError()

    if not contacts:
        return "No contacts yet. Use 'add' to create."

    upcoming_birthdays = contacts.get_upcoming_birthdays(days)

    if not upcoming_birthdays:
        return f"No birthdays in the next {days} day(s). Use 'add-birthday' to set."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming_birthdays)
