import datetime
from psycopg2 import Date


def validate_date_of_birth(value: Date) -> None:
    """Validate that the date of birth is not in the future.
    Validate that the user is at least 16 years old.

    Args:
        value (Date): The date of birth to validate.

    Raises:
        ValueError: If the date of birth is in the future.
    """
    if value > datetime.datetime.now().date():
        raise ValueError("Date of birth cannot be in the future")
    if datetime.datetime.now().year - value.year < 16:
        raise ValueError("User must be at least 16 years old")

def validate_phone_number(value: str) -> None:
    """Validate that the phone number is in a valid international format.

    Args:
        value (str): The phone number to validate.

    Raises:
        ValueError: If the phone number is not in a valid format.
    """
    import re
    pattern = re.compile(r'^\+\d{1,3}\d{4,14}(?:x.+)?$')
    if not pattern.match(value):
        raise ValueError("Invalid phone number format. It should be in international format, e.g., +234123456789")
    