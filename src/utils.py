import re
import datetime
from toolz import curry

@curry
def validate_shortcode(shortcode_length_limit, shortcode):
    return shortcode is not None and len(shortcode) == shortcode_length_limit

@curry
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
    counter = get_counter_value()  # TODO catch possible failure
    encoded = []
    while counter > 0:
        val = counter % base
        encoded.append(characters[val])
        counter = counter // base  # double slash returns the integer in python3
    # since `encoded` has reversed order of base62 id, reverse ret before return it
    return "".join(encoded[::-1])


def get_now_in_iso8601():
    # - Notice there is a bug when using astimezone() on utc time.
    #   datetime.datetime.utcnow().astimezone().isoformat() gives an incorrect result
    # - datetime.datetime.now().isoformat("T") doesn't add the Z in the specs
    # - not sure if microseconds were required to be in a precision of 3, or 6 is ok 🤷‍♂️
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")