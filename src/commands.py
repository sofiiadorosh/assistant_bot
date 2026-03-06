from models import AddressBook, Record
from decorators import input_error
from exceptions import ArgumentInvalidError


def hello(args, contacts):
    return "How can I help you?"


def exit_program(args, contacts):
    return "exit"


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
    if not contacts:
        return "No contacts yet. Use 'add' to create."

    upcoming_birthdays = contacts.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays yet. Use 'add-birthday' to set."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming_birthdays)
