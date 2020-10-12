from flask import Flask, request
from src.short_url_pipeline import short_url_pipeline, short_url_pipeline_record

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/shorten", methods=["POST"])
def post_shortcode():
    pipeline_result = short_url_pipeline.get_shortened_url(request.json)
    return "success" if pipeline_result.success else "fail"


# @app.route("/shortcode/stats")
# def get_shortcode_stats():
#     return "Hello, World!"


# @app.route("/shortcode")
# def redirect_shortcode():
#     #  return redirect(url_for('login'))
#     return "Hello, World!"