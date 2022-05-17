import dotenv
import os
import sheets_handler

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    if request.values.get("Body") is not None:
        request_message = request.values.get("Body").lower().strip()
        from_number = request.values.get("From")
        print(f"Incoming message: {request_message}")
        print(f"From phone number: {from_number}")

        # Start our TwiML response
        resp = MessagingResponse()

        phone_numbers = os.environ["PHONE_NUMBERS"].split(",") # build list of phone numbers

        # If sender is recognized, give appropriate reply
        if from_number in phone_numbers:
            message = sheets_handler.GoogleSheetsApiHandler().get_sheet_data(request_message)
        else:
            message = "Invalid message request." # TODO: add help message here
        
        resp.message(message)
        return str(resp)
    
    return "<p>No data, chief.</p>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
