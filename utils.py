"""Utility functions for the application."""

import re


def validate_phone_numbers(input_string):
    """Validate phone numbers in a string."""
    pattern = r'^\+\d{1,3}\d{10}(,\+\d{1,3}\d{10})*$'
    if re.match(pattern, input_string):
        return True

    return False
