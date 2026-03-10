from collections import UserDict
from datetime import datetime, timedelta
import re


SATURDAY_WEEKDAY = 5
WEEK_DAYS = 7


class AddressBookError(Exception):
    pass


class RecordNotFoundError(AddressBookError):
    pass


class InvalidPhoneError(AddressBookError):
    pass


class InvalidBirthdayError(AddressBookError):
    pass


class InvalidNameError(AddressBookError):
    pass


class InvalidEmailError(AddressBookError):
    pass


class InvalidAddressError(AddressBookError):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value or len(str(value).strip()) < 2:
            raise InvalidNameError("Name must be at least 2 characters long.")
        self._value = str(value).strip()


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not re.fullmatch(r"\d{10,}", value):
            raise InvalidPhoneError("Phone number must contain at least 10 digits.")
        self._value = value


class Email(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.fullmatch(email_regex, value):
            raise InvalidEmailError("Invalid email format (e.g., user@example.com).")
        self._value = value


class Address(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = str(value).strip()
        if len(value) < 3:
            raise InvalidAddressError("Address should be at least 3 characters long.")
        self._value = value


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            self._value = birthday_date
        except ValueError:
            raise InvalidBirthdayError("Invalid date format. Use DD.MM.YYYY.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [
            existing_phone
            for existing_phone in self.phones
            if existing_phone.value != phone
        ]

    def edit_phone(self, old_phone, new_phone):
        for existing_phone in self.phones:
            if existing_phone.value == old_phone:
                existing_phone.value = new_phone
                return

    def find_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                return existing_phone

        return None

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def set_email(self, email):
        self.email = Email(email)

    def set_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        email = str(self.email) if self.email else "Not set"
        address = str(self.address) if self.address else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}, email: {email}, address: {address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record_by_name(self, name):
        for stored, record in self.data.items():
            if stored.lower() == name.lower():
                return record
        return None

    def find_record_by_phone(self, phone):
        return [
            contact
            for contact in self.data.values()
            if any(phone == str(contact_phone.value) for contact_phone in contact.phones)
        ]

    def find_record_by_email(self, email):
        return [
            contact
            for contact in self.data.values()
            if contact.email and email in contact.email.value.lower()
        ]

    def find_record_by_address(self, address):
        return [
            contact
            for contact in self.data.values()
            if contact.address and address in contact.address.value.lower()
        ]

    def find_record_by_all(self, query):
        return [
            contact
            for contact in self.data.values()
            if (
                query in contact.name.value.lower()
                or any(query in str(phone.value) for phone in contact.phones)
                or (contact.email and query in contact.email.value.lower())
                or (contact.address and query in contact.address.value.lower())
            )
        ]

    def find_record(self, field, query):
        methods = {
            "name": self.find_record_by_name,
            "phone": self.find_record_by_phone,
            "email": self.find_record_by_email,
            "address": self.find_record_by_address,
            "all": self.find_record_by_all,
        }
        method = methods.get(field)
        if not method:
            return []
        return method(query)

    def delete_record(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days):
        today_date = datetime.today().date()

        end_date = today_date + timedelta(days=days)

        upcoming_birthdays = []

        for contact in self.data.values():
            if not contact.birthday:
                continue

            name = contact.name.value
            birthday = contact.birthday.value

            year = today_date.year

            while True:
                try:
                    birthday_date = datetime(year, birthday.month, birthday.day).date()
                except ValueError:
                    year += 1
                    continue

                if birthday_date > end_date:
                    break

                if birthday_date >= today_date:
                    congratulation_date = birthday_date
                    weekday = congratulation_date.weekday()

                    if weekday >= SATURDAY_WEEKDAY:
                        congratulation_date += timedelta(days=WEEK_DAYS - weekday)

                    upcoming_birthdays.append(
                        {"name": name, "congratulation_date": congratulation_date}
                    )

                year += 1

        upcoming_birthdays.sort(key=lambda x: x["congratulation_date"])

        for item in upcoming_birthdays:
            item["congratulation_date"] = item["congratulation_date"].strftime(
                "%d.%m.%Y"
            )

        return upcoming_birthdays
