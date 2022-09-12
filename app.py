import dotenv
import os

from flask import Flask, request
from sheets_handler import GoogleSheetsApiHandler
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent to our Twilio number
    if request.values.get("Body") is not None:
        request_message = request.values.get("Body").lower().strip()
        from_number = request.values.get("From")
        print(f"Incoming message: {request_message}")
        print(f"From phone number: {from_number}")


        phone_numbers = os.environ["PHONE_NUMBERS"].split(",") # build list of phone numbers

        # If sender is recognized, give appropriate reply
        if from_number in phone_numbers:
            gsh = GoogleSheetsApiHandler()
            message = gsh.get_message(request_message)
            # Start our TwiML response
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)
        
        return
        
    else:
        return "<p>No data, chief.</p>"


if __name__ == "__main__":
    app.run(debug=True)
