import pytest
from src.utils import validate_url, shorten_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("dummy_string", False),
        ("https://www.facebook.com/", True),
        ("http://www.facebook.com/", True),
        ("https://www.facebook.com", True),
        ("https://www.facebook💤.com", False),
        ("https://www.facebook .com", False),
        ("ht://www.facebook .com", False),
        ("http://www.facebook.com:8080", True),
    ],
)
def test_url_validation(url, expected):
    assert validate_url(url) == expected


@pytest.mark.parametrize(
    "unwrapped_url,id,expected",
    [
        ("https://www.facebook.com/", 1, "1"),
        ("https://www.facebook.com/", 63, "11"),
        ("https://www.facebook.com/", 9000, "2la"),
		("https://www.facebook.com/", 14776336, "10000"),
		("https://www.facebook.com/", 14776335, "ZZZZ"),
    ],
)
def test_url_shortnening(unwrapped_url, id, expected):
    getCounter = lambda: id

    assert shorten_url(getCounter, unwrapped_url) == expected
