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

    password = password.lower()

    patterns = [

        # Numbers
        "012",
        "123",
        "234",
        "345",
        "456",
        "567",
        "678",
        "789",

        # Letters
        "abc",
        "bcd",
        "cde",
        "def",
        "xyz",

        # Keyboard patterns
        "qwe",
        "asd",
        "zxc"

    ]

    password = password.lower()

    return any(
        x in password
        for x in patterns
    )


def has_common_word_pattern(password):

    common_words = [

        "password",
        "admin",
        "welcome",
        "hello",
        "world",
        "letmein",
        "qwerty"

    ]

    password = password.lower()

    for word in common_words:

        if word in password:
            return True

    return False


def has_repeated_pattern(password):

    password = password.lower()

    length = len(password)

    for size in range(4, length // 3 + 1):

        for i in range(length - size):

            pattern = password[i:i+size]

            if password.count(pattern) >= 3:
                return True

    return False


def has_dictionary_match(password, common_passwords):

    password = password.lower()

    found = 0

    for word in common_passwords:

        word = word.strip().lower()

        if len(word) >= 5 and word.isalpha():

            if word in password:
                found += 1

    return found >= 2


def has_name_pattern(password, names):

    password = password.lower()

    for name in names:

        if len(name) >= 4 and name in password:
            return True

    return False


def has_year_pattern(password):

    return bool(
        re.search(
            r"(19|20)\d{2}",
            password
        )
    )
