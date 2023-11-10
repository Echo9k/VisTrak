# validation.py
from datetime import datetime
import re


def layout(row, expected_length):
    expected_columns = expected_length  # Update the number based on your file structure
    return len(row) == expected_columns

def email(email):
    # Regex for general email validation
    general_email_regex = r"(^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z0-9])$"
    
    # Regex specifically for Gmail addresses
    gmail_email_regex = r"(^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@gmail\.com$)"
    
    # If the domain is 'gmail.com', use the Gmail-specific regex
    if email.lower().endswith('@gmail.com'):
        return re.match(gmail_email_regex, email) is not None
    else:  # Otherwise, use the general regex
        return re.match(general_email_regex, email) is not None

def date(date_str):
    if date_str and date_str != '-':
        try:
            # The date format in the CSV file
            datetime.strptime(date_str, '%d/%m/%Y %H:%M')
            return True
        except ValueError:
            # If an exception is caught, it means the date string is invalid
            return False
    return True
