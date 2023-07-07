"""Google Sheets API Handler"""

import google.auth
import json
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Get Google API Scopes from environment variable
SCOPES = os.getenv("SCOPES")
if SCOPES is not None:
    SCOPES = SCOPES.split(",")
else:
    print("Invalid Google API Scopes in environment variable SCOPES.")
    exit(1)

# Get Google Sheets Configuration file from environment variable
SHEETS_CONFIG_FILE = os.getenv("SHEETS_CONFIG_FILE")
if SHEETS_CONFIG_FILE is None:
    print("Google Sheets Configuration file not specified in environment")
    exit(1)


class GoogleSheetsApiHandler:
    """Google Sheets API Handler"""
    def __init__(self) -> None:
        """Initialize Google Sheets API Handler"""
        # this will pick up GOOGLE_APPLICATION_CREDENTIALS environment variable
        # https://google-auth.readthedocs.io/en/master/user-guide.html
        credentials, _ = google.auth.default(scopes=SCOPES)
        try:
            # create a sheets api service from credentials
            sheets_api_service = build('sheets', 'v4', credentials=credentials)
            self.sheet = sheets_api_service.spreadsheets()

        except HttpError as err:
            print(err)
            raise

    def _load_sheets_config(self, sheets_config_file: str) -> dict:
        """Return dict from Google Sheets Configuration json file"""
        if os.path.isfile(sheets_config_file):
            with open(sheets_config_file, "r") as sheets_config:
                return json.load(sheets_config)

        else:
            print("Google Sheets Configuration file not found.")
            exit(1)

    def _get_sheet_data(self, sheets_config_data: dict,
                        request_message: str) -> tuple:
        """Return spreadsheet_id and sheet_range_dict from
        sheets_config_data"""
        if "spreadsheets" in sheets_config_data:
            for spreadsheet in sheets_config_data["spreadsheets"]:
                if "spreadsheet_id" in spreadsheet and \
                        "sheet_ranges" in spreadsheet:
                    for sheet_range in spreadsheet["sheet_ranges"]:
                        if sheet_range["request_message"] == request_message:
                            return spreadsheet["spreadsheet_id"], sheet_range

        else:
            print("No spreadsheets in Google Sheets Configuration file.")
            exit(1)

    def get_message(self, request_message: str) -> str:
        """Return message from Google Sheets"""
        sheets_config_data = self._load_sheets_config(SHEETS_CONFIG_FILE)
        if bool(sheets_config_data):
            spreadsheet_id, sheet_range_dict = (
                self._get_sheet_data(sheets_config_data, request_message))
            if bool(sheet_range_dict):
                response_message = sheet_range_dict["response_message"]
                result = self.sheet.values().get(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_range_dict["range"],
                    valueRenderOption="UNFORMATTED_VALUE"
                    ).execute()
                values = result.get('values', [])

                if not values:
                    print('No data found.')
                    return ""

                # only set up to return data from one cell
                for row in values:
                    for cell in row:
                        # TODO leave formatting to Sheets API
                        message = f"{response_message}: ${cell:,.2f}"
                        return message

            else:
                print("Invalid message")
                return "Invalid message"  # TODO add help message here

        else:
            print("sheets_configuration.json file not loaded properly.")
            exit(1)
