import pytest
from src.short_url_pipeline import (
    short_url_pipeline,
    short_url_pipeline_record,
)


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
    result = short_url_pipeline.read_request_into_record(request)
    assert (
        result.url == url
        and result.desired_shortCode == shortcode
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
    result.desired_shortCode = shortcode
    short_url_pipeline.validate_parameters(result)
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
    result.desired_shortCode = shortcode
    short_url_pipeline.get_shortCode(
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

    result = short_url_pipeline.get_shortened_url(
        get_counter, increment_counter, get_stored_code, set_shortCode, request
    )

    assert (
        result.success == expectedSuccess
        and result.apiCode == expectedApiCode
        and result.desired_shortCode == shortcode
        and result.shortcode == expectedCode
    )
