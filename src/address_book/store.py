from pickle import dump, load

from src.address_book.models import AddressBook


FILENAME = "address_book.pkl"


def save_data(book, filename=FILENAME):
    with open(filename, "wb") as fh:
        dump(book, fh)


def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as fh:
            return load(fh)
    except FileNotFoundError:
        return AddressBook()
        