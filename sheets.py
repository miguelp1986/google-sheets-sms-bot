import ast
import dotenv
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from twilio.rest import Client


# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDIT_CARD_PAYMENT_VALUES = ast.literal_eval(os.environ["CREDIT_CARD_PAYMENT_VALUES"])

def main() -> None:
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
        result = sheet.values().get(
            spreadsheetId=os.environ["SAMPLE_SPREADSHEET_ID"], \
            range=os.environ["NET_BUDGET_RANGE"], \
            valueRenderOption=value_render_option \
            ).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            for cell in row:
                message = "Budget left for month: ${:.2f}".format(cell)
                phone_number = os.environ["PERSONAL_PHONE_NUMBER"]

        # Write example
        value_input_option = "USER_ENTERED"
        value_range_body = {
            "range": os.environ["TEST_RANGE"],
            "majorDimension": "COLUMNS",
            "values": [
                os.environ["TEST_VALUES"] TODO fix invalid data value error
            ]
        }

        request = service.spreadsheets().values().update(
            spreadsheetId=os.environ["SAMPLE_SPREADSHEET_ID"], \
            range=os.environ["TEST_RANGE"], \
            valueInputOption=value_input_option, \
            body=value_range_body)
        response = request.execute()

    except HttpError as err:
        print(err)


