import re


def encode_url(url):
    return url


def validate_url(url):
    regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # Domain
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or IPv4
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


def shorten_url(get_counter_value, unwrapped_url):
    # base 62 characters
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    counter = get_counter_value()
    encoded = []
    while counter > 0:
        val = counter % base
        encoded.append(characters[val])
        counter = counter // base  # double slash returns the integer in python3
    # since `encoded` has reversed order of base62 id, reverse ret before return it
    return "".join(encoded[::-1])
