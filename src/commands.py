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
| edit-email <name> <new_email>                 | Update existing email                          |
| add-address <name> <address>                  | Add address to contact                         |
| edit-address <name> <new_address>              | Update existing address                       |
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
        (name,) = args
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
        (name,) = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add' to create."

    if not record.birthday:
        return f"Birthday for '{name}' is not set."

    return str(record.birthday)


@input_error
def add_email(args, contacts: AddressBook):
    try:
        name, email = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        record = Record(name)
        contacts.add_record(record)
        record.add_email(email)
        return f"Contact '{name}' added with email."

    if record.email:
        return f"Contact '{name}' already has an email. Use 'edit-email' to change it."

    record.add_email(email)
    return f"Email added for contact '{name}'."


@input_error
def edit_email(args, contacts: AddressBook):
    try:
        name, new_email = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add-contact' to create."

    if not record.email:
        return f"Contact '{name}' doesn't have an email yet. Use 'add-email' first."

    record.update_email(new_email)
    return f"Email updated for contact '{name}'."


@input_error
def add_address(args, contacts: AddressBook):
    if not args:
        raise ArgumentInvalidError

    name, *address_parts = args
    address = " ".join(address_parts)

    record = contacts.find_record(name)

    if record is None:
        record = Record(name)
        record.add_address(address)
        contacts.add_record(record)
        return f"Contact '{name}' added with address."

    if record.address:
        return (
            f"Contact '{name}' already has an address. Use 'edit-address' to change it."
        )

    record.add_address(address)
    return f"Address added for contact '{name}'."


@input_error
def edit_address(args, contacts: AddressBook):
    if not args:
        raise ArgumentInvalidError

    name, *address_parts = args
    address = " ".join(address_parts)

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add-contact' to create."

    if not record.address:
        return f"Contact '{name}' doesn't have an address yet. Use 'add-address' first."

    record.update_address(address)
    return f"Address updated for contact '{name}'."


@input_error
def delete_contact(args, contacts: AddressBook):
    if not args:
        raise ArgumentInvalidError

    name = args[0]
    if name not in contacts:
        return f"Contact '{name}' not found."

    contacts.delete_record(name)
    return f"Contact '{name}' deleted successfully."


@input_error
def get_upcoming_birthdays(args, contacts: AddressBook):
    if not args:
        raise ArgumentInvalidError

    (days,) = args

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
    return "\n".join(
        f"{entry['name']}: {entry['congratulation_date']}"
        for entry in upcoming_birthdays
    )
