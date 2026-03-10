from src.exceptions import ArgumentInvalidError, DaysInvalidError
from src.address_book.models import (
    AddressBookError,
    InvalidPhoneError,
    InvalidEmailError,
    InvalidBirthdayError,
    RecordNotFoundError,
    AddressBook,
)
from src.note_book.models import NoteBook
from src.address_book.store import save_data as save_address_book
from src.note_book.store import save_data as save_note_book


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DaysInvalidError:
            return "Days must be a non-negative integer."
        except (
            InvalidPhoneError,
            InvalidEmailError,
            InvalidBirthdayError,
            RecordNotFoundError,
        ) as e:
            return str(e)
        except ArgumentInvalidError:
            return "Provide all needed arguments to run a command."
        except AddressBookError as e:
            return e
        except Exception as e:
            return f"Error: {e}"

    return inner

def persist_data(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)

        if result == "exit":
            save_address_book(args[1])
            save_note_book(args[2])
            return result

        if isinstance(args[1], AddressBook):
            save_address_book(args[1])
        elif isinstance(args[1], NoteBook):
            save_note_book(args[1])

        return result
    return inner
