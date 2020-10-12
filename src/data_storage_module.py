from toolz import curry
from src.utils import get_now_in_iso8601

@curry
def get_unwrapped_url_in_db(shortcodes_dict, shortcode):
    if shortcode in shortcodes_dict:
        return True, shortcodes_dict[shortcode]
    else:
        return False, None


@curry
def store_shortCode_in_db(shortcodes_dict, metadata_dict, shortcode, url):
    shortcodes_dict[shortcode] = url
    metadata_dict[shortcode] = {
        "redirectCount": 0,
        "lastRedirect": None,
        "created": get_now_in_iso8601(),
    }


@curry
def update_metadata_in_db(metadata_dict, shortcode):
    if shortcode in metadata_dict:
        metadata_dict[shortcode]["redirectCount"] += 1
        metadata_dict[shortcode]["lastRedirect"] = get_now_in_iso8601()
    else:
        print("need to insert this key first")


@curry
def read_metadata_in_db(metadata_dict, shortcode):
    if shortcode in metadata_db:
        item = metadata_db[shortcode]
        return {
            "redirectCount": item["redirectCount"],
            "lastRedirect": item["lastRedirect"],
            "created": item["created"],
        }
    else:
        return None