from __future__ import print_function

import dotenv
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load .env file
try:
    dotenv.load_dotenv()
except Exception as e:
    print(e)
    sys.exit(1)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ["SAMPLE_SPREADSHEET_ID"]
NET_BUDGET_RANGE = os.environ["NET_BUDGET_RANGE"]
CREDIT_CARD_BALANCE_RANGE = os.environ["CREDIT_CARD_BALANCE_RANGE"]
CREDIT_CARD_PAYMENT_RANGE = os.environ["CREDIT_CARD_PAYMENT_RANGE"]

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
                print(f"Budget left for month: {cell}")

        # Write example
        value_input_option = "USER_ENTERED"
        value_range_body = {
            "range": CREDIT_CARD_PAYMENT_RANGE,
            "majorDimension": "COLUMNS",
            "values": [
                [1, 2, 3, 4, 5, 6, 7, 8]
            ]
        }

        request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, \
            range=CREDIT_CARD_PAYMENT_RANGE, valueInputOption=value_input_option, body=value_range_body)
        response = request.execute()

        print(response)


    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
