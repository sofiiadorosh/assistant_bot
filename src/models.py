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
    def __init__(self, phone):
        self.phone = phone
        super().__init__(self.value)

    @property
    def phone(self):
        return self.value

    @phone.setter
    def phone(self, phone):
        if not re.fullmatch(r'\d{10}', phone):
            raise InvalidPhoneError("Phone number must contain exactly 10 digits.")
        self.value = phone


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

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [
            existing_phone for existing_phone in self.phones
            if existing_phone.value != phone
        ]

    def edit_phone(self, old_phone, new_phone):
        for existing_phone in self.phones:
            if existing_phone.value == old_phone:
                existing_phone.phone = new_phone
                return
        raise PhoneNotFoundError("Phone number not found.")

    def find_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                return existing_phone

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


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

                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date
                    })

                year += 1

        upcoming_birthdays.sort(key=lambda x: x["congratulation_date"])

        for item in upcoming_birthdays:
            item["congratulation_date"] = item["congratulation_date"].strftime("%d.%m.%Y")

        return upcoming_birthdays
