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


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    request_message = request.values.get("Body").lower()
    from_number = request.values.get("From")
    print(f"Incoming message: {request_message}")
    print(f"From phone number: {from_number}")

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if from_number == os.environ["PERSONAL_PHONE_NUMBER1"] or from_number == os.environ["PERSONAL_PHONE_NUMBER2"]:
        message = sheets_handler.GoogleSheetsApiHandler().get_sheet_data(request_message)
        resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
