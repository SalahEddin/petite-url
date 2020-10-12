from flask import Flask, request, redirect
from toolz import pipe, partial, curry
from dotenv import load_dotenv
import os
from src.shorten_url_module import shorten_url_module, short_url_pipeline_record
from src.utils import get_now_in_iso8601
from src.data_storage_module import (
    get_unwrapped_url_in_db,
    read_metadata_in_db,
    store_shortCode_in_db,
    update_metadata_in_db,
)
from src.counter_module import (
    get_counter_value,
    increment_counter_value,
    set_counter_value,
)

###########################
#### Environment Variables and globals
###########################

shortCodes_db = {}
metadata_db = {}

load_dotenv()
set_counter_value(int(os.getenv("COUNTER_STARTING_VALUE")))
SHORTCODE_LENGTH_LIMIT = int(os.getenv("SHORTCODE_LENGTH_LIMIT"))
print(SHORTCODE_LENGTH_LIMIT)
###########################
#### Partial Functions
###########################

read_metadata = read_metadata_in_db(metadata_db)
update_metadata = update_metadata_in_db(metadata_db)
get_unwrapped_url = get_unwrapped_url_in_db(shortCodes_db)
store_in_shortcode_db = store_shortCode_in_db(shortCodes_db, metadata_db)
shorten_url_db_loaded = shorten_url_module.get_shortened_url(
    SHORTCODE_LENGTH_LIMIT,
    get_counter_value,
    increment_counter_value,
    get_unwrapped_url,
    store_in_shortcode_db,
)
get_shortcode_redirect_url = shorten_url_module.get_unwrapped_url(
    SHORTCODE_LENGTH_LIMIT, update_metadata, get_unwrapped_url
)

###########################
#### Routes
###########################

app = Flask(__name__)


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
