from collections import UserDict
import re
from typing import Optional, Union


class Field:
    def __init__(self, value: Union[str, int]) -> None:
        """Base class for fields in a record"""

        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Class for storing the name of a contact"""


class Phone(Field):
    def __init__(self, value: str) -> None:
        """
        Class for storing a phone number with validation.

        :param value: The phone number (must be 10 digits).
        :raises ValueError: If the phone number is not 10 digits.
        """
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        """Class for storing contact information, including name and phone numbers.

        :param name: The name of the contact.
        """
        self.name = Name(name.strip())
        self.phones = []

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the contact.

        :param phone: The phone number to add.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the contact.

        :param phone: The phone number to remove.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number.

        :param old_phone: The phone number to be replaced.
        :param new_phone: The new phone number.
        :raises ValueError: If the old phone number is not found.
        """
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone number in the contact.

        :param phone: The phone number to find.
        :return: The Phone object if found, else None.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        """Add a record to the address book.

        :param record: The Record object to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Find a record by name.

        :param name: The name of the contact.
        :return: The Record object if found, else None.
        """
        return self.data.get(name.strip())

    def delete(self, name: str) -> None:
        """Delete a record by name.

        :param name: The name of the contact to delete.
        :raises ValueError: If the record is not found.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found")
