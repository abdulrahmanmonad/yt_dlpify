from random import choices
from string import ascii_letters, digits


def generate_random_string_without_digits(*, string_length: int = 9) -> str:
    return "".join(choices(ascii_letters, k=string_length))


def generate_random_string_with_digits(*, string_length: int = 9) -> str:
    return "".join(choices(ascii_letters + digits, k=string_length))


def generate_random_url(*, string_length: int = 9) -> str:
    return (
        "https://"
        + generate_random_string_without_digits(string_length=string_length)
        + ".com"
    )
