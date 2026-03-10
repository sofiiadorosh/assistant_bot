import json
from pathlib import Path

from src.address_book.models import AddressBook, Record, AddressBookError


_BASE_DIR = Path(__file__).resolve().parent.parent.parent
FILENAME = _BASE_DIR / "samples" / "contacts.json"


def save_data(book, filename=FILENAME):
    contacts = {}
    for name, record in book.data.items():
        contacts[name] = {
            "name": record.name.value,
            "phones": [phone.value for phone in record.phones],
            "birthday": record.birthday.value.strftime("%d.%m.%Y") if record.birthday else None,
            "email": record.email.value if record.email else None,
            "address": record.address.value if record.address else None,
        }
    with open(Path(filename), "w", encoding="utf-8") as fh:
        json.dump(contacts, fh, indent=2, ensure_ascii=False)


def load_data(filename=FILENAME):
    try:
        with open(Path(filename), "r", encoding="utf-8") as fh:
            contacts = json.load(fh)
    except FileNotFoundError:
        return AddressBook()
    except json.JSONDecodeError:
        return AddressBook()

    book = AddressBook()
    for name, contact in contacts.items():
        if not isinstance(contact, dict) or "name" not in contact:
            continue
        try:
            record = Record(contact["name"])
            for phone in contact.get("phones", []):
                record.add_phone(str(phone))
            if contact.get("birthday"):
                record.set_birthday(contact["birthday"])
            if contact.get("email"):
                record.set_email(contact["email"])
            if contact.get("address"):
                record.set_address(contact["address"])
            book.add_record(record)
        except (TypeError, ValueError, KeyError, AddressBookError):
            continue
    return book
