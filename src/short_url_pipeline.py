from toolz import pipe, curry
from src.url_utils import validate_url, shorten_url

# TODO move to environment
SHORT_URL_LENGTH = 6

REQUEST_BODY_URL_KEY = "url"
REQUEST_BODY_SHORTCODE_KEY = "shortCode"


class short_url_pipeline_record:
    url = None
    desired_shortCode = None
    success = True
    shortCode = None
    apiCode = 200
    message = None


class short_url_pipeline:
    def validate_parameters(result):
        if result.url is None:
            result.success = False
            result.apiCode = 400
            result.message = "URL is not present."
        elif not validate_url(result.url):
            result.success = False
            result.apiCode = 400
            result.message = "URL is not in a valid format."
        elif (
            result.desired_shortCode is not None
            and len(result.desired_shortCode) != SHORT_URL_LENGTH
        ):
            result.success = False
            result.apiCode = 412
            result.message = "short code is not in a valid format."
        return result

    # TODO split into generation if not there and the storage
    @curry
    def get_shortCode(
        get_counter, increment_counter, get_stored_shortCode, store_shortCode, result
    ):
        if not result.success:
            return result
        isFound = False
        if result.desired_shortCode is not None:
            isFound, _ = get_stored_shortCode(result.desired_shortCode)
        if isFound:
            result.success = False
            result.apiCode = 409
            result.message = "shortCode is already in use."
        else:
            result.shortCode = (
                shorten_url(get_counter, result.url)
                if result.desired_shortCode is None
                else result.desired_shortCode
            )
            if result.shortCode is not None:
                store_shortCode(result.shortCode, result.url)
                increment_counter()
            else:
                result.success = False
                result.apiCode = 500
                result.message = "Could not generate shortCode."
        return result

    def read_request_into_record(request_body):
        result = short_url_pipeline_record()
        result.desired_shortCode = (
            request_body[REQUEST_BODY_SHORTCODE_KEY]
            if REQUEST_BODY_SHORTCODE_KEY in request_body
            else None
        )
        result.url = (
            request_body[REQUEST_BODY_URL_KEY]
            if REQUEST_BODY_URL_KEY in request_body
            else None
        )
        result.apiCode = 200
        result.shortCode = None
        result.message = None
        result.success = True
        return result

    def get_shortened_url(
        get_counter,
        increment_counter,
        get_stored_shortCode,
        store_shortCode,
        request_body,
    ):
        # TODO try/catch
        get_shortCode = short_url_pipeline.get_shortCode(
            get_counter, increment_counter, get_stored_shortCode, store_shortCode
        )

        return pipe(
            request_body,
            short_url_pipeline.read_request_into_record,
            short_url_pipeline.validate_parameters,
            get_shortCode,
        )
