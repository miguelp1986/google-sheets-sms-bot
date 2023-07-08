"""Main application file for Google Sheets SMS bot."""

import config
import os

from flask import Flask, request
from sheets_handler import GoogleSheetsApiHandler
from twilio.twiml.messaging_response import MessagingResponse
from utils import validate_phone_numbers

# load environment variables from .env file
config.load_env()

# Get Flask host and port from environment variables
FLASK_HOST = os.getenv("FLASK_HOST")
if FLASK_HOST is None:
    print("No FLASK_HOST environment variable found.")
    exit(1)

FLASK_PORT = os.getenv("FLASK_PORT")
if FLASK_PORT is None:
    print("No FLASK_PORT environment variable found.")
    exit(1)

# Get list of phone numbers from environment variable
PHONE_NUMBERS = os.getenv("PHONE_NUMBERS")
if PHONE_NUMBERS is not None and validate_phone_numbers(PHONE_NUMBERS):
    PHONE_NUMBERS = PHONE_NUMBERS.split(",")

else:
    print("Invalid phone numbers in environment variable PHONE_NUMBERS.")
    exit(1)

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent to our Twilio number
    request_body = request.values.get("Body")
    if request_body is not None:
        request_message = request_body.lower().strip()
        from_number = request.values.get("From")
        if from_number is not None:
            print(f"Incoming message: {request_message}")
            print(f"From phone number: {from_number}")

        else:
            print("No sender phone number.")
            exit(1)

        # If sender is recognized, give appropriate reply
        if from_number in PHONE_NUMBERS:
            gsh = GoogleSheetsApiHandler()
            message = gsh.get_message(request_message)
            # Start our TwiML response
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)

        else:
            return "<p>Sorry, I don't know you.</p>"

    else:
        return "<p>No data, chief.</p>"


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
