from flask import Flask, request, jsonify, redirect
import datetime
from src.shorten_url_module import shorten_url_module, short_url_pipeline_record
from src.utils import get_now_in_iso8601

app = Flask(__name__)

###########################
#### Globals
###########################
shortCodes_db = {}
metadata_db = {}
counter = 1


def increment_counter():
    global counter
    counter += 1


def get_counter():
    global counter
    return counter


def get_unwrapped_url_in_db(shortcode):
    if shortcode in shortCodes_db:
        return True, shortCodes_db[shortcode]
    else:
        return False, None


def store_shortCode_in_db(shortcode, url):
    global shortCodes_db
    shortCodes_db[shortcode] = url
    metadata_db[shortcode] = {
        "redirectCount": 0,
        "lastRedirect": None,
        "created": get_now_in_iso8601(),
    }


def update_metadata(shortcode):
    global metadata_db
    if shortcode in metadata_db:
        metadata_db[shortcode]["redirectCount"] += 1
        metadata_db[shortcode]["lastRedirect"] = get_now_in_iso8601()
    else:
        print("need to insert this key first")


def read_metadata(shortcode):
    if shortcode in metadata_db:
        item = metadata_db[shortcode]
        return {
            "redirectCount": item["redirectCount"],
            "lastRedirect": item["lastRedirect"],
            "created": item["created"],
        }
    else:
        return None


shorten_url_db_loaded = shorten_url_module.get_shortened_url(
    get_counter, increment_counter, get_unwrapped_url_in_db, store_shortCode_in_db
)

get_shortcode_redirect_url = shorten_url_module.get_unwrapped_url(
    update_metadata, get_unwrapped_url_in_db
)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/shorten", methods=["POST"])
def post_shortcode():
    pipeline_result = shorten_url_db_loaded(request.json)
    return (
        ({"shortcode": pipeline_result.shortcode}, 201)
        if pipeline_result.success
        else (pipeline_result.message, pipeline_result.apiCode)
    )


@app.route("/shortcode")
def redirect_shortcode():
    pipeline_result = get_shortcode_redirect_url(request.json)
    return (
        redirect(pipeline_result.url)
        if pipeline_result.success
        else (pipeline_result.message, pipeline_result.apiCode)
    )


@app.route("/shortcode/stats")
def get_shortcode_stats():
    if "shortcode" not in request.json:
        return "shortcode not present", 400
    search_result = read_metadata(request.json["shortcode"])
    if search_result is None:
        return "shortcode not found", 404
    return search_result, 200
