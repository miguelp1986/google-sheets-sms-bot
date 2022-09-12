# Google Sheets SMS Bot

This project allows you to setup an SMS bot that allows you to get cell data from Google Sheets. It uses Google Authentication, Google Sheets API, and the Twilio Messaging API.

## Google API Setup

### Authentication

- In order to authenticate with your Google API account, a service account is needed. 
- Follow the steps here to create one: https://cloud.google.com/iam/docs/creating-managing-service-accounts
- Once your service account has been created, create an account key: https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating
- Once created, download the json file. You will need to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of this file.

### Setup Permissions for Google Sheets

- In order for your Google Service Account to be able to access your Google Sheets, you will need to explicitly grant it permissions. From your Google Cloud dashboard, get your service account email and share your Google Sheet with that email address.

### Google Sheets Configuration

The Google Sheets configuration that is being used here allows for multiple Google Sheets to be accessed,
and allows for SMS messages to be customized for each Google Sheet. Below is an example json snippet which
shows you how to customize your own message request, response, and sheet data. More information on how to
use Google Sheet ranges can be found here: https://developers.google.com/sheets/api/guides/concepts#cell

Example:

```json
{
    "spreadsheets": 
    [
        {
            "spreadsheet_id": "",
            "spreadsheet_ranges": 
            [
                {
                    "request_message": "",
                    "response_message": "",
                    "range": ""
                },
            ]
        }
    ]
}
```

## Twilio Setup
