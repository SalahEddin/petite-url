import pytest
from src.url_utils import validate_url


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
def test_answer(url, expected):
    assert validate_url(url) == expected