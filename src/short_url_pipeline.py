from toolz import pipe, curry
from src.utils import validate_url, validate_shortcode, shorten_url

REQUEST_BODY_URL_KEY = "url"
REQUEST_BODY_SHORTCODE_KEY = "shortcode"


class short_url_pipeline_record:
    url = None
    requested_shortcode = None
    success = True
    shortcode = None
    apiCode = 200
    message = None


class short_url_pipeline:

    ###########################
    ### Pure functions
    ###########################

    def validate_shorten_parameters(result):
        if result.url is None:
            result.success = False
            result.apiCode = 400
            result.message = "URL is not present."
        elif not validate_url(result.url):
            result.success = False
            result.apiCode = 400
            result.message = "URL is not in a valid format."
        elif result.requested_shortcode is not None and not validate_shortcode(
            result.requested_shortcode
        ):
            result.success = False
            result.apiCode = 412
            result.message = "short code is not in a valid format."
        return result

    def validate_unwrap_parameters(result):
        if result.requested_shortcode is None or not validate_shortcode(
            result.requested_shortcode
        ):
            # TODO set from another module
            result.success = False
            result.apiCode = 412
            result.message = "shortcode not in a valid format."
        return result

    @curry
    def search_unwrapped_url(get_stored_shortcode, result):
        if result is None or not result.success:
            return result
        isFound, unwrapped_url = get_stored_shortcode(result.requested_shortcode)
        if not isFound:
            result.success = False
            result.apiCode = 404
            result.message = "shortcode not found."
        else:
            result.url = unwrapped_url
            result.apiCode = 302
        return result

    @curry
    def get_shortCode(
        get_counter, increment_counter, get_stored_shortCode, store_shortCode, result
    ):
        if not result.success:
            return result
        isFound = False
        if result.requested_shortcode is not None:
            isFound, _ = get_stored_shortCode(result.requested_shortcode)
        if isFound:
            result.success = False
            result.apiCode = 409
            result.message = "shortcode is already in use."
        else:
            result.shortcode = (
                shorten_url(get_counter, result.url)
                if result.requested_shortcode is None
                else result.requested_shortcode
            )
            if result.shortcode is not None:
                store_shortCode(result.shortcode, result.url)
                increment_counter()
            else:
                result.success = False
                result.apiCode = 500
                result.message = "Could not generate shortcode."
        return result

    def read_request_into_record(request_body):
        result = short_url_pipeline_record()
        result.requested_shortcode = (
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
        result.shortcode = None
        result.message = None
        result.success = True
        return result

    # Method to allow running a method in a pipeline
    @curry
    def run_if_successful(func, record):
        if record is not None and record.success:
            func(record.requested_shortcode)
        return record

    ###########################
    ### Pipelines
    ###########################

    @curry
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
            short_url_pipeline.validate_shorten_parameters,
            get_shortCode,
        )

    @curry
    def get_unwrapped_url(
        register_entry_hit,
        get_stored_shortCode,
        request_body,
    ):
        # TODO try/catch
        get_url = short_url_pipeline.search_unwrapped_url(get_stored_shortCode)
        update_shortcode_metadata = short_url_pipeline.run_if_successful(
            register_entry_hit
        )

        return pipe(
            request_body,
            short_url_pipeline.read_request_into_record,
            short_url_pipeline.validate_unwrap_parameters,
            get_url,
            update_shortcode_metadata,
        )
