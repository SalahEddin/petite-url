from flask import Flask, request, redirect
from toolz import pipe, partial, curry
from src.shorten_url_module import shorten_url_module, short_url_pipeline_record
from src.utils import get_now_in_iso8601
from src.data_storage_module import (
    get_unwrapped_url_in_db,
    read_metadata_in_db,
    store_shortCode_in_db,
    update_metadata_in_db,
)

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
    return counter


###########################
#### Partial Functions
###########################

read_metadata = read_metadata_in_db(metadata_db)
update_metadata = update_metadata_in_db(metadata_db)
get_unwrapped_url = get_unwrapped_url_in_db(shortCodes_db)
store_in_shortcode_db = store_shortCode_in_db(shortCodes_db, metadata_db)
shorten_url_db_loaded = shorten_url_module.get_shortened_url(
    get_counter, increment_counter, get_unwrapped_url, store_in_shortcode_db
)
get_shortcode_redirect_url = shorten_url_module.get_unwrapped_url(
    update_metadata, get_unwrapped_url
)

###########################
#### Routes
###########################


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/test")
def test():
    global shortCodes_db
    print(shortCodes_db)
    store_in_shortcode_db("123456", "http://ww.ww.ww")
    print(shortCodes_db)
    return "1 "


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
