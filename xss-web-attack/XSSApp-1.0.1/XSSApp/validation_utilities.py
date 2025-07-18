from typing import Callable
from bs4 import BeautifulSoup

import re


MAIL_REGEX = re.compile(r"""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""")
PHONE_REGEX = re.compile(r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")
NAME_REGEX = re.compile(r"^[\w ,.'-]+$", re.UNICODE | re.IGNORECASE)
FILE_NAME_REGEX = re.compile(r"^[\w_]+\.[\w_]+$", re.UNICODE | re.IGNORECASE)


def regex_validator(func: Callable, name: str):
    def validate(element):
        if func(element) is None:
            raise ValueError(f"{name} validation failed")
        return True
    return validate


def generate_regex_validator(regex: re.Pattern, name: str) -> Callable:
    return regex_validator(lambda element: re.match(regex, element), name)


def get_all_attributes(s: BeautifulSoup):
    attrs = []
    for elm in s.find_all():
        attrs += list(elm.attrs.keys())
    return attrs


def has_on_attribute(attribute_name: str):
    return attribute_name.lower().startswith("on")


def validate_message(message: str):
    parsed = BeautifulSoup(message, 'html.parser')
    if parsed.findChildren("script"):
        raise ValueError("message contains scripts!")
    all_attributes = get_all_attributes(parsed)
    if any(has_on_attribute(elem) for elem in all_attributes):
        raise ValueError("An on attribute was detected!")
    return True


def is_valid_uploaded_file_name(file_name: str):
    ALLOWED_EXTENSIONS = {"htm", "html"}
    if not isinstance(file_name, str):
        return False
    if FILE_NAME_REGEX.match(file_name) is not None:
        return file_name.split(".")[1] in ALLOWED_EXTENSIONS
    return False
