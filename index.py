from flask import Flask, request, jsonify, redirect
import datetime
from src.short_url_pipeline import short_url_pipeline, short_url_pipeline_record

app = Flask(__name__)

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


def update_metadata(shortcode):
    global metadata_db
    if shortcode in metadata_db:
        metadata_db[shortcode].redirectCount += 1
        metadata_db[shortcode].lastRedirect = datetime.datetime.now()
    else:
        print("need to insert this key first")


shorten_url_db_loaded = short_url_pipeline.get_shortened_url(
    get_counter, increment_counter, get_unwrapped_url_in_db, store_shortCode_in_db
)

get_shortcode_redirect_url = short_url_pipeline.get_unwrapped_url(
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
        redirect(pipeline_result.url, pipeline_result.apiCode)
        if pipeline_result.success
        else (pipeline_result.message, pipeline_result.apiCode)
    )


# @app.route("/shortcode/stats")
# def get_shortcode_stats():
#     return "Hello, World!"
