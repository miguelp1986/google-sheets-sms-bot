import dotenv
import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)

# If modifying scope, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsApiHandler:
    """."""
    def __init__(self) -> None:
        """."""
        self.creds = self._get_creds()
        try:
            self.sheets_api_service = build('sheets', 'v4', credentials=self.creds)
            self.sheet = self.sheets_api_service.spreadsheets()
    
        except HttpError as err:
            print(err)
            raise


    def _get_creds(self):
        """."""
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
        
        return creds

    
    def _load_sheets_config(self, sheets_config_file:str) -> dict:
        """Return dict from Google Sheets Configuration json file"""
        if os.path.isfile(sheets_config_file):
            with open(sheets_config_file, "r") as sheets_config:
                return json.load(sheets_config)

        return {}


    def _get_sheet_range(self, sheets_config_data:dict, request_message:str) -> dict:
        """Get dict with the Gooogle Sheet range for the corresponding request message"""
        if "spreadsheets" in sheets_config_data:
            for spreadsheet in sheets_config_data["spreadsheets"]:
                if "spreadsheet_id" in spreadsheet and "sheet_ranges" in spreadsheet \
                    and spreadsheet["spreadsheet_id"] == os.environ["SPREADSHEET_ID"]:
                    for sheet_range in spreadsheet["sheet_ranges"]:
                        if sheet_range["request_message"] == request_message:
                            return sheet_range

        return {}


    def get_sheet_data(self, request_message:str) -> str:
        """."""
        sheets_config_data = self._load_sheets_config("sheets_configuration.json")
        if bool(sheets_config_data):
            sheet_range_dict = self._get_sheet_range(sheets_config_data, request_message)
            if bool(sheet_range_dict) and "request_message" in sheet_range_dict and \
                sheet_range_dict["request_message"] == request_message:
                response_message = sheet_range_dict["response_message"]
                result = self.sheet.values().get(
                    spreadsheetId=os.environ["SPREADSHEET_ID"], \
                    range=sheet_range_dict["range"], \
                    valueRenderOption="UNFORMATTED_VALUE" \
                    ).execute()
                values = result.get('values', [])

                if not values:
                    print('No data found.')
                    return ""
                
                # only set up to return data from one cell
                for row in values:
                    for cell in row:
                        message = f"{response_message}: ${cell:,.2f}"
                        return message
        
        return ""
