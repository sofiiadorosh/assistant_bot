from src.exceptions import ArgumentInvalidError, DaysInvalidError
from src.models import (
    AddressBookError,
    InvalidPhoneError,
    InvalidEmailError,
    InvalidBirthdayError,
    RecordNotFoundError,
)


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
