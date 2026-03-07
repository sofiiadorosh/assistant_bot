from src.models import AddressBookError
from src.exceptions import ArgumentInvalidError, DaysInvalidError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DaysInvalidError:
            return "Days must be a non-negative integer."
        except ArgumentInvalidError:
            return "Provide all needed arguments to run a command."
        except AddressBookError as e:
            return e
        except Exception as e:
            return f"Error: {e}"

    return inner
