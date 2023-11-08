# validation.py
# Define validation functions
import re
from datetime import datetime


def layout(row):
    expected_columns = 15  # Update the number based on your file structure
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
    if date_str == '-':
        return True  # '-' is a placeholder for no date
    try:
        # The date strings in the data 'DD/MM/YYYY HH:MM'
        datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        # If there is an unexpected string that's not a placeholder, consider it invalid
        return False
