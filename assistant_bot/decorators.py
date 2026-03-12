from assistant_bot.exceptions import ArgumentInvalidError, DaysInvalidError
from assistant_bot.address_book.models import (
    AddressBookError,
    InvalidPhoneError,
    InvalidEmailError,
    InvalidBirthdayError,
    RecordNotFoundError,
    AddressBook,
)
from assistant_bot.note_book.models import (
    NoteBook,
    InvalidTitleError,
    InvalidContentError,
)
from assistant_bot.address_book.store import save_data as save_address_book
from assistant_bot.note_book.store import save_data as save_note_book


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DaysInvalidError:
            return "Days must be a non-negative integer."
        except (
            RecordNotFoundError,
            InvalidPhoneError,
            InvalidEmailError,
            InvalidBirthdayError,
            InvalidTitleError,
            InvalidContentError
        ) as e:
            return str(e)
        except ArgumentInvalidError:
            return "Provide all needed arguments to run a command."
        except AddressBookError as e:
            return str(e)
        except Exception as e:
            return f"Error: {e}"

    return inner

def persist_data(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        contacts = kwargs.get("contacts")
        notes = kwargs.get("notes")
        
        if isinstance(contacts, AddressBook):
            save_address_book(contacts)
        
        if isinstance(notes, NoteBook):
            save_note_book(notes)

        return result
    return inner
