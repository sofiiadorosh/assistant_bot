from collections import UserDict
from datetime import datetime, timedelta
import re


SATURDAY_WEEKDAY = 5
WEEK_DAYS = 7


class AddressBookError(Exception):
    pass


class InvalidPhoneError(AddressBookError):
    pass


class InvalidBirthdayError(AddressBookError):
    pass


class PhoneNotFoundError(AddressBookError):
    pass


class RecordNotFoundError(AddressBookError):
    pass


class InvalidNameError(AddressBookError):
    pass


class InvalidEmailError(AddressBookError):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value or len(value.strip()) < 2:
            raise InvalidNameError("Name must be at least 2 characters long.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not re.fullmatch(r"\d{10,}", new_value):
            raise InvalidPhoneError("Phone number must contain at least 10 digits.")
        self._value = new_value


class Email(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.fullmatch(email_regex, new_value):
            raise InvalidEmailError("Invalid email format (e.g., user@example.com).")
        self._value = new_value


class Address(Field):
    def __init__(self, value):
        if len(value) < 3:
            raise AddressBookError("Address should be at least 3 characters long.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, birthday):
        self.birthday = birthday
        super().__init__(self.value)

    @property
    def birthday(self):
        return self.value

    @birthday.setter
    def birthday(self, birthday):
        try:
            birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError:
            raise InvalidBirthdayError("Invalid date format. Use DD.MM.YYYY.")
        self.value = birthday_date

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
        raise PhoneNotFoundError("Phone number not found.")

    def find_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                return existing_phone

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def update_email(self, new_email):
        self.email = Email(new_email)

    def update_address(self, new_address):
        self.address = Address(new_address)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        email = str(self.email) if self.email else "Not set"
        address = str(self.address) if self.address else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}, email: {email}, address: {address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record(self, name):
        if name not in self.data:
            return None
        return self.data[name]

    def delete_record(self, name):
        if name not in self.data:
            raise RecordNotFoundError(f"Contact '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        today_date = today.date()
        in_seven_days_date = (today + timedelta(days=WEEK_DAYS)).date()

        upcoming_birthdays = []

        for contact in self.data.values():
            name = contact.name.value

            if not contact.birthday:
                continue

            birthday_datetime = contact.birthday.value

            try:
                birthday_date = datetime(
                    year=today_date.year,
                    month=birthday_datetime.month,
                    day=birthday_datetime.day,
                )
            except ValueError:
                print(
                    f"Cannot find birthday this year for {name}: {birthday_datetime}."
                )
                continue

            if birthday_date.date() < today_date:
                birthday_date = birthday_date.replace(year=today_date.year + 1)

            if today_date <= birthday_date.date() < in_seven_days_date:
                weekday = birthday_date.weekday()

                if weekday >= SATURDAY_WEEKDAY:
                    birthday_date += timedelta(days=WEEK_DAYS - weekday)

                upcoming_birthdays.append(
                    {
                        "name": name,
                        "congratulation_date": birthday_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming_birthdays
