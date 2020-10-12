import pytest
from src.shorten_url_module import (
    shorten_url_module,
    short_url_pipeline_record,
)
from src.utils import validate_shortcode, validate_url


@pytest.mark.parametrize(
    "url,shortcode",
    [
        (None, None),
        ("htt://www.facebook.com/", None),
        ("https://www.facebook.com/", None),
        ("https://www.facebook.com/", "123456"),
        ("https://www.facebook.com/", "12345"),
    ],
)
def test_record_building(url, shortcode):
    request = {"url": url, "shortcode": shortcode}
    result = shorten_url_module.read_request_into_record(request)
    assert (
        result.url == url
        and result.requested_shortcode == shortcode
        and result.success == True
        and result.apiCode == 200
        and result.shortcode is None
    )


@pytest.mark.parametrize(
    "url,shortcode,expectedSuccess,expectedApiCode",
    [
        (None, None, False, 400),
        ("htt://www.facebook.com/", None, False, 400),
        ("https://www.facebook.com/", None, True, 200),
        ("https://www.facebook.com/", "123456", True, 200),
        ("https://www.facebook.com/", "12345", False, 412),
    ],
)
def test_url_validation(url, shortcode, expectedSuccess, expectedApiCode):
    result = short_url_pipeline_record()
    result.url = url
    result.requested_shortcode = shortcode
    validate_shortcode_with_limit = validate_shortcode(6)
    shorten_url_module.validate_shorten_parameters(
        validate_shortcode_with_limit, validate_url, result
    )
    assert result.success == expectedSuccess and result.apiCode == expectedApiCode


@pytest.mark.parametrize(
    "shortcode,expectedSuccess,expectedApiCode",
    [
        ("123456", True, 200),
        (None, False, 412),
        ("1234567", False, 412),
        ("12345", False, 412),
    ],
)
def test_shortcode_validation(shortcode, expectedSuccess, expectedApiCode):
    result = short_url_pipeline_record()
    result.success = True
    result.apiCode = 200
    result.requested_shortcode = shortcode
    validate_shortcode_with_limit = validate_shortcode(6)

    shorten_url_module.validate_unwrap_parameters(validate_shortcode_with_limit, result)
    assert result.success == expectedSuccess and result.apiCode == expectedApiCode


@pytest.mark.parametrize(
    "shortcode,alreadyExists,expectedSuccess,expectedApiCode",
    [
        ("aws123", False, True, 200),
        ("aws123", True, False, 409),
    ],
)
def test_shortCode_retrieval(
    shortcode, alreadyExists, expectedSuccess, expectedApiCode
):
    def get_counter():
        return 1

    def increment_counter():
        return

    def get_stored_code(shortcode):
        return (True, "https://www.facebook.com/") if alreadyExists else (False, None)

    def set_shortCode(shortcode, url):
        return

    result = short_url_pipeline_record()
    result.url = "https://www.facebook.com/"
    result.requested_shortcode = shortcode
    shorten_url_module.get_shortCode(
        get_counter, increment_counter, get_stored_code, set_shortCode, result
    )
    assert result.success == expectedSuccess and result.apiCode == expectedApiCode


@pytest.mark.parametrize(
    "url,shortcode,alreadyExists,expectedSuccess,expectedApiCode,expectedCode",
    [
        (None, "aws123", False, False, 400, None),
        (None, None, True, False, 400, None),
        ("https://www.facebook.com/", "aws123", False, True, 200, "aws123"),
        ("https://www.facebook.com/", None, False, True, 200, "1"),
        ("https://www.facebook.com/", "aws123", True, False, 409, None),
        ("https://www.facebook.com/", "aws123456", True, False, 412, None),
    ],
)
def test_shortCode_pipeline(
    url, shortcode, alreadyExists, expectedSuccess, expectedApiCode, expectedCode
):
    def get_counter():
        return 1

    def increment_counter():
        return

    def get_stored_code(shortcode):
        return (True, "https://www.facebook.com/") if alreadyExists else (False, None)

    def set_shortCode(shortcode, url):
        return

    request = {"url": url, "shortcode": shortcode}

    result = shorten_url_module.get_shortened_url(
        6, get_counter, increment_counter, get_stored_code, set_shortCode, request
    )

    assert (
        result.success == expectedSuccess
        and result.apiCode == expectedApiCode
        and result.requested_shortcode == shortcode
        and result.shortcode == expectedCode
    )


@pytest.mark.parametrize(
    "shortcode,expectedSuccess,expectedApiCode,expectedUrl",
    [
        ("aws123", False, 404, None),
        ("aws1241", False, 412, None),
        ("aws124", True, 302, "https://www.facebook.com/"),
    ],
)
def test_shortCode_pipeline(shortcode, expectedSuccess, expectedApiCode, expectedUrl):
    def get_stored_code(shortcode):
        return (
            (True, "https://www.facebook.com/")
            if shortcode == "aws124"
            else (False, None)
        )

    def update_metadata(shortcode):
        return

    request = {"shortcode": shortcode}

    result = shorten_url_module.get_unwrapped_url(
        6, update_metadata, get_stored_code, request
    )

    assert (
        result.success == expectedSuccess
        and result.apiCode == expectedApiCode
        and result.url == expectedUrl
        # TODO if there's time use Mock to confirm update_metadata
        # is called only in successful cases
    )
