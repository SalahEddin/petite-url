from toolz import pipe
from src.url_utils import validate_url, shorten_url

# TODO move to environment
SHORT_URL_LENGTH = 6


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
    # need to curry
    def get_shortCode(
        get_counter, increment_counter, get_stored_shortCode, store_shortCode, result
    ):
        if not result.success:
            return result
        isFound, _ = get_stored_shortCode(result.desired_shortCode)
        if isFound:
            result.success = False
            result.apiCode = 409
            result.message = "shortCode is already in use."
        else:
            result.shortCode = shorten_url(get_counter, result.url)
            if result.shortCode is not None:
                store_shortCode(result.shortCode, result.url)
                increment_counter()
            else:
                result.success = False
                result.apiCode = 500
                result.message = "Could not generate shortCode."
        return result

    def get_shortened_url(
        get_counter,
        increment_counter,
        get_stored_shortCode,
        store_shortCode,
        request_body,
    ):
        result = short_url_pipeline_record()
        # TODO try/catch
        # pipe(result, )
        # # compose( validate_parameters, if shortened_exists: fail else
        # (if no deired generate else not, get_shortcode, save_shortcode, save_metadata, (retrun (code, message))

        # if "shortcode" in request.json:
        #     # shortcode has a length of 6 characters and will contain only
        #     # alphanumeric characters or underscores, and shouldn't be in use

        #     # compose (validate_shortcode, is_shortcode_in_use)
        #     print("shortcode")
        # else:
        #     # compose (generate_shortcode)
        #     print(request.json)
        # compose (save_shortcode, save_metadata, (retrun (code, message)))
        return result
