import dotenv
import os

from flask import Flask, request, redirect
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
    incoming_message = request.values.get('Body', None)
    from_number = request.values.get("From")
    print(f"Incoming message: {incoming_message}")
    print(f"From phone number: {from_number}")

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if from_number == os.environ["PERSONAL_PHONE_NUMBER1"] or from_number == os.environ["PERSONAL_PHONE_NUMBER2"]:
        resp.message("Only you two should receive this message")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
