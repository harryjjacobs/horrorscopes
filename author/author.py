#!/usr/bin/env python3

import base64
from datetime import datetime, timedelta
import logging
import os
import flask
import openai
from google.cloud import datastore

# Write some in a horror theme and others as more realistic, less fantasy-based, suspense or thrillers that are dark.

PROMPT = """
Imagine you are a horoscope writer but for "horrorscopes" where the horoscope has a dark theme.
Vary between classic/fantasy-based horror, realistic suspense/thriller, mundane horror (everyday tedium), and dark comedy in general. 
The horrorscopes should also contain absurdly specific details or scenarios, much unlike regular horoscopes, to the point of being comedic in their specificity - try to avoid vague notions.
Leave some of them without a happy or positive ending or any advice.
These are just for fun, as a joke and not to be taken seriously.
Generate a horoscope for all 12 star signs for {}.
Only output each one in the following format and contain no other text:
{{star sign here in lowercase}}
{{the generated horrorscope here}}
---
"""

logging.basicConfig(level=logging.INFO)

if os.getenv("OPENAI_API_KEY"):
    logging.info("Reading openai api key from env var OPENAI_API_KEY")
    openai.api_key = os.getenv("OPENAI_API_KEY")
elif os.path.exists("/etc/secrets/openai-api-key"):
    logging.info("Reading openai api key from /etc/secrets/openai-api-key")
    openai.api_key = open("/etc/secrets/openai-api-key").read()


def create(date: str):
    """
    Generate new horrorscope for today for each zodiac sign.

    Args:
        date (str): date to generate horrorscope for in format dd/mm/yyyy
    """

    zodiacs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
               "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]

    horrorscopes = {zodiac: "" for zodiac in zodiacs}

    # get horrorscope for today for all zodiac signs
    prompt = PROMPT.format(date)
    # use gpt3 to generate horrorscope
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
    )

    if response.choices is None or len(response.choices) == 0:
        logging.error("Empty response from gpt3")
        return

    if response.choices[0].finish_reason != "stop":
        logging.error(
            f"Response from gpt3 did not finish. Reason: {response.choices[0].finish_reason}")
        return

    response_items = response.choices[0].message.content.strip().split("---")
    for item in response_items:
        zodiac = item.strip().split("\n")[0].lower().strip()
        if zodiac in zodiacs:
            horrorscopes[zodiac] = item.strip().split("\n")[1].strip()
        else:
            logging.warning(
                f"Zodiac sign {zodiac} not found in gtp response: {response.choices[0]}")

    print(horrorscopes)
    return horrorscopes


app = flask.Flask(__name__)


@app.route("/create", methods=["POST"])
def http_create():
    args = flask.request.args
    if not "date" in args:
        print("No date provided. Using today's date.")
        date = datetime.now().strftime("%d/%m/%Y")
    elif args["date"] == "today":
        date = datetime.now().strftime("%d/%m/%Y")
    elif args["date"] == "tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    else:
        try:
            datetime.strptime(date, "%d/%m/%Y")
            date = args["date"]
        except:
            print("Invalid date provided. Using today's date.")
            date = None

    logging.info(f"Generating horrorscopes for {date}")
    horrorscopes = create(date)
    client = datastore.Client()
    key = client.key("horrorscope")
    entity = datastore.Entity(
        key=key, exclude_from_indexes=list(horrorscopes.keys()))
    entity["date"] = date
    for zodiac, horrorscope in horrorscopes.items():
        entity[zodiac] = horrorscope
    client.put(entity)

    return ("", 204)  # success, no content


if __name__ == "__main__":
    logging.info("Generating horrorscopes for today")
    create(datetime.now().strftime("%d/%m/%Y"))
