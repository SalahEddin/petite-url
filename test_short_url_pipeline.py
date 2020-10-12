import pytest
from src.short_url_pipeline import short_url_pipeline, short_url_pipeline_record


@pytest.mark.parametrize(
    "url,shortCode,expectedSuccess,expectedApiCode",
    [
        (None, None, False, 400),
        ("htt://www.facebook.com/", None, False, 400),
        ("https://www.facebook.com/", None, True, 200),
        ("https://www.facebook.com/", "123456", True, 200),
        ("https://www.facebook.com/", "12345", False, 412),
    ],
)
def test_url_validation(url, shortCode, expectedSuccess, expectedApiCode):
    result = short_url_pipeline_record()
    result.url = url
    result.desired_shortCode = shortCode
    short_url_pipeline.validate_parameters(result)
    assert result.success == expectedSuccess and result.apiCode == expectedApiCode


@pytest.mark.parametrize(
    "shortCode,alreadyExists,expectedSuccess,expectedApiCode",
    [
        ("aws123", False, True, 200),
        ("aws123", True, False, 409),
    ],
)
def test_shortCode_retrieval(
    shortCode, alreadyExists, expectedSuccess, expectedApiCode
):
    def get_counter():
        return 1

    def increment_counter():
        print("Increment")

    def get_stored_code(shortCode):
        return (True, "https://www.facebook.com/") if alreadyExists else (False, None)

    def set_shortCode(shortCode, url):
        print(f"setting {shortCode} as ref to {url}")

    result = short_url_pipeline_record()
    result.url = "https://www.facebook.com/"
    result.desired_shortCode = shortCode
    short_url_pipeline.get_shortCode(
        get_counter, increment_counter, get_stored_code, set_shortCode, result
    )
    assert result.success == expectedSuccess and result.apiCode == expectedApiCode