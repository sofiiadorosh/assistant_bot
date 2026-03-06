from models import AddressBookError
from exceptions import ArgumentInvalidError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArgumentInvalidError:
            return "Provide all needed arguments to run a command."
        except AddressBookError as e:
            return e
        except Exception as e:
            return f"Error: {e}"

    return inner
