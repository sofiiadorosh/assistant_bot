from src.models import (
    AddressBookError,
    InvalidPhoneError,
    InvalidEmailError,
    InvalidBirthdayError,
    RecordNotFoundError,
)
from src.exceptions import ArgumentInvalidError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
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
            return str(e)
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return inner
