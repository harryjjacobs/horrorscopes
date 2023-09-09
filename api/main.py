from datetime import datetime
import logging
import flask
from flask_cors import CORS
from google.cloud import datastore

logging.basicConfig(level=logging.INFO)


app = flask.Flask(__name__)
CORS(app)


@app.route("/api/horrorscope", methods=["GET"])
def index():
    zodiac = flask.request.args.get("zodiac")
    date = flask.request.args.get("date")

    try:
        datetime.strptime(date, "%d/%m/%Y")
    except:
        logging.error(f"Invalid date provided: {date}")
        return ("", 400)

    # fetch today's horrorscope from the db
    client = datastore.Client()
    query = client.query(kind="horrorscope")
    query.add_filter("date", "=", date)
    horrorscope = list(query.fetch())

    if len(horrorscope) == 0:
        return ("No horrorscopes found for this date", 404)

    if zodiac not in horrorscope[0]:
        return ("Zodiac not found in db", 404)

    return (horrorscope[0][zodiac], 200)
