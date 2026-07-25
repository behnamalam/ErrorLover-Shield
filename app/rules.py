import re


def has_upper(password):
    return bool(re.search(r"[A-Z]", password))


def has_lower(password):
    return bool(re.search(r"[a-z]", password))


def has_digit(password):
    return bool(re.search(r"[0-9]", password))


def has_symbol(password):
    return bool(re.search(r"[^A-Za-z0-9]", password))


def has_repeated_chars(password):
    return bool(re.search(r"(.)\1\1", password))


def has_sequential_pattern(password):
    patterns = [
        "123",
        "234",
        "345",
        "456",
        "789",
        "abc",
        "bcd",
        "xyz"
    ]

    for pattern in patterns:
        if pattern in password.lower():
            return True

    return False