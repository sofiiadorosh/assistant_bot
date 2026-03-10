from src.exceptions import ArgumentInvalidError, DaysInvalidError
from src.address_book.models import AddressBook, Record
from src.decorators import input_error, persist_data

@input_error
@persist_data
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
@persist_data
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
@persist_data
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
@persist_data
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
@persist_data
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
@persist_data
def add_address(args, contacts: AddressBook):
    try:
        name, *address_parts = args
        if not address_parts:
            raise ValueError

        address = " ".join(address_parts)
    except ValueError:
        raise ArgumentInvalidError

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
@persist_data
def edit_address(args, contacts: AddressBook):
    try:
        name, *address_parts = args
        if not address_parts:
            raise ValueError

        address = " ".join(address_parts)
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.find_record(name)

    if record is None:
        return f"Contact '{name}' does not exist. Use 'add-contact' to create."

    if not record.address:
        return f"Contact '{name}' doesn't have an address yet. Use 'add-address' first."

    record.update_address(address)
    return f"Address updated for contact '{name}'."


@input_error
@persist_data
def delete_contact(args, contacts: AddressBook):
    try:
        (name,) = args
    except ValueError:
        raise ArgumentInvalidError

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
