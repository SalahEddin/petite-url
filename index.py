from flask import Flask, request, jsonify
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


shorten_url_db_loaded = short_url_pipeline.get_shortened_url(
    get_counter, increment_counter, get_unwrapped_url_in_db, store_shortCode_in_db
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


# @app.route("/shortcode/stats")
# def get_shortcode_stats():
#     return "Hello, World!"


# @app.route("/shortcode")
# def redirect_shortcode():
#     #  return redirect(url_for('login'))
#     return "Hello, World!"
