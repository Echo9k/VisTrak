import re
from datetime import datetime

email_regex = re.compile(r"(^[a-zA-Z0-9_.-]+(@gmail\.com$|[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-zA-Z0-9])$)")


def layout(row, expected_length):
    """
    Checks if the length of the input row matches the expected length.

    Args:
        row (iterable): The row to be validated.
        expected_length (int): The expected length of the row.

    Returns:
        bool: True if the length of the row matches the expected length, False otherwise.
    """
    return len(row) == expected_length


def email(email_address):
    """
    Checks if the input email address is valid according to a predefined regex pattern.

    Args:
        email_address (str): The email address to be validated.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    email_to_check = (email_address
                      if email_address.islower()
                      else email_address.lower())
    return email_regex.match(email_to_check) is not None


def date(date_str):
    """
    Checks if the input string represents a valid date in the format '%d/%m/%Y %H:%M'.

    Args:
        date_str (str): The string to be validated as a date.

    Returns:
        bool: True if the input string is a valid date, False otherwise.
    """
    if not date_str or date_str == '-' or len(date_str) != 16:
        return False
    try:
        datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False
