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

    record = contacts.get_record(name)

    if record is None:
        record = Record(name)
        contacts.add_record(record)
        record.add_phone(phone)
        return f"Contact '{name}' added."

    record.add_phone(phone)
    return f"Contact '{name}' updated."


@input_error
@persist_data
def edit_contact(args, contacts: AddressBook):
    try:
        name, old_phone, new_phone = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    phone = record.find_phone(old_phone)
    if phone is None:
        return f"Contact '{name}' does not have phone '{old_phone}'. Use 'add-contact' to add it."

    record.edit_phone(old_phone, new_phone)

    return f"Contact '{name}' updated."


@input_error
def show_phone(args, contacts: AddressBook):
    try:
        (name,) = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    return "; ".join(str(phone) for phone in record.phones)


@input_error
def find_contact(args, contacts: AddressBook):
    try:
        if not args:
            raise ValueError
        field, *rest = ("all", *args) if len(args) == 1 else args
        if not rest:
            raise ValueError
        value = " ".join(rest).strip()
        if not value:
            raise ValueError
        field = field.lower()
        value = value.lower()
        finders = {"name", "phone", "email", "address", "all"}
        if field not in finders:
            raise ValueError
    except ValueError:
        raise ArgumentInvalidError

    result = contacts.find_record(field, value)
    if result is None:
        records = []
    elif isinstance(result, list):
        records = result
    else:
        records = [result]

    if not records:
        return f"No contacts found with {field} '{value}'."
    return "\n".join(str(record) for record in records)


def show_all(args, contacts: AddressBook):
    if not contacts:
        return "No contacts yet. Use 'add-contact' to create."

    return "\n".join(str(record) for record in contacts.values())


@input_error
@persist_data
def add_birthday(args, contacts: AddressBook):
    try:
        name, birthday = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    record.set_birthday(birthday)
    return f"Contact '{name}' updated."


@input_error
def show_birthday(args, contacts: AddressBook):
    try:
        (name,) = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    if not record.birthday:
        return f"Contact '{name}' has no birthday set."

    return str(record.birthday)


@input_error
@persist_data
def add_email(args, contacts: AddressBook):
    try:
        name, email = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        record = Record(name)
        contacts.add_record(record)
        record.set_email(email)
        return f"Contact '{name}' added."

    if record.email:
        return f"Contact '{name}' already has an email. Use 'edit-email' to change it."

    record.set_email(email)
    return f"Contact '{name}' updated."


@input_error
@persist_data
def edit_email(args, contacts: AddressBook):
    try:
        name, new_email = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    if not record.email:
        return f"Contact '{name}' doesn't have an email yet. Use 'add-email' to set it."

    record.set_email(new_email)
    return f"Contact '{name}' updated."


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

    record = contacts.get_record(name)

    if record is None:
        record = Record(name)
        record.set_address(address)
        contacts.add_record(record)
        return f"Contact '{name}' added."

    if record.address:
        return (
            f"Contact '{name}' already has an address. Use 'edit-address' to change it."
        )

    record.set_address(address)
    return f"Contact '{name}' updated."


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

    record = contacts.get_record(name)

    if record is None:
        return f"Contact '{name}' not found. Use 'add-contact' to create."

    if not record.address:
        return f"Contact '{name}' doesn't have an address yet. Use 'add-address' to set it."

    record.set_address(address)
    return f"Contact '{name}' updated."


@input_error
@persist_data
def delete_contact(args, contacts: AddressBook):
    try:
        (name,) = args
    except ValueError:
        raise ArgumentInvalidError

    record = contacts.get_record(name)
    if record is None:
        return f"Contact '{name}' not found."

    contacts.delete_record(record.name.value)
    return f"Contact '{name}' deleted."


@input_error
def get_upcoming_birthdays(args, contacts: AddressBook):
    days = 7
    if args:
        try:
            (days,) = args
            days = int(days)
            if days < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise DaysInvalidError()

    if not contacts:
        return "No contacts yet. Use 'add-contact' to create."

    upcoming_birthdays = contacts.get_upcoming_birthdays(days)

    if not upcoming_birthdays:

        return f"No birthdays in the next {days} day(s). Use 'add-birthday' to set."
    return "\n".join(
        f"{entry['name']}: {entry['congratulation_date']}"
        for entry in upcoming_birthdays
    )
