import dotenv
import google.auth
import json
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Load .env file
try:
    dotenv.load_dotenv()
except Exception as err:
    print(err)
    raise

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsApiHandler:
    """."""
    def __init__(self) -> None:
        """."""
        # this will pick up GOOGLE_APPLICATION_CREDENTIALS env var
        # https://google-auth.readthedocs.io/en/master/user-guide.html
        credentials, _ = google.auth.default(scopes=SCOPES) 
        try:
            sheets_api_service = build('sheets', 'v4', credentials=credentials)
            self.sheet = sheets_api_service.spreadsheets()
    
        except HttpError as err:
            print(err)
            raise

    
    def _load_sheets_config(self, sheets_config_file:str) -> dict:
        """Return dict from Google Sheets Configuration json file"""
        if os.path.isfile(sheets_config_file):
            with open(sheets_config_file, "r") as sheets_config:
                return json.load(sheets_config)

        return {} # TODO: raise error instead


    def _get_sheet_data(self, sheets_config_data:dict, request_message:str) -> tuple:
        """Get dict with the Gooogle Sheet range for the corresponding request message"""
        if "spreadsheets" in sheets_config_data:
            for spreadsheet in sheets_config_data["spreadsheets"]:
                if "spreadsheet_id" in spreadsheet and "sheet_ranges" in spreadsheet:
                    for sheet_range in spreadsheet["sheet_ranges"]:
                        if sheet_range["request_message"] == request_message:
                            return spreadsheet["spreadsheet_id"], sheet_range

        return (None, None) # TODO: raise error instead


    def get_message(self, request_message:str) -> str:
        """."""
        sheets_config_data = self._load_sheets_config("sheets_configuration.json")
        if bool(sheets_config_data):
            spreadsheet_id, sheet_range_dict = self._get_sheet_data(sheets_config_data, request_message)
            if bool(sheet_range_dict):
                response_message = sheet_range_dict["response_message"]
                result = self.sheet.values().get(
                    spreadsheetId=spreadsheet_id, \
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
                        message = f"{response_message}: ${cell:,.2f}" # TODO: leave formatting to Sheets API
                        return message
            
            else:
                print("Invalid message")
                return "Invalid message" # TODO: add help message here
        
        else:
            print("sheets_configuration.json file not loaded properly.") # TODO: raise error instead
