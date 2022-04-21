import ast
from email import message
from venv import create
import dotenv
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from twilio.rest import Client

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ["SAMPLE_SPREADSHEET_ID"]
NET_BUDGET_RANGE = os.environ["NET_BUDGET_RANGE"]
CREDIT_CARD_BALANCE_RANGE = os.environ["CREDIT_CARD_BALANCE_RANGE"]
CREDIT_CARD_PAYMENT_RANGE = os.environ["CREDIT_CARD_PAYMENT_RANGE"]
CREDIT_CARD_PAYMENT_VALUES = ast.literal_eval(os.environ["CREDIT_CARD_PAYMENT_VALUES"])
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
PERSONAL_PHONE_NUMBER = os.environ["PERSONAL_PHONE_NUMBER"]
FATHIA_PHONE_NUMBER = os.environ["FATHIA_PHONE_NUMBER"]

TWILIO_SERVICE_SID = os.environ["TWILIO_SERVICE_SID"]
TWILIO_CONVERSATION_SID = os.environ["TWILIO_CONVERSATION_SID"]

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Read example
        sheet = service.spreadsheets()
        value_render_option = "UNFORMATTED_VALUE"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, \
                                    range=NET_BUDGET_RANGE, \
                                    valueRenderOption=value_render_option).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            for cell in row:
                message = "Budget left for month: ${:.2f}".format(cell)
                phone_number = PERSONAL_PHONE_NUMBER
                twilio_conversation(sms_message=message, phone_number=phone_number)

        # # Write example
        # value_input_option = "USER_ENTERED"
        # value_range_body = {
        #     "range": CREDIT_CARD_PAYMENT_RANGE,
        #     "majorDimension": "COLUMNS",
        #     "values": [
        #         CREDIT_CARD_PAYMENT_VALUES
        #     ]
        # }

        # request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, \
        #     range=CREDIT_CARD_PAYMENT_RANGE, valueInputOption=value_input_option, body=value_range_body)
        # response = request.execute()

        # print(response)

    except HttpError as err:
        print(err)


def twilio_conversation(sms_message:str, phone_number:str) -> str:
    """."""
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=sms_message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=phone_number
                    )


if __name__ == '__main__':
    main()
