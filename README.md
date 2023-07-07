# Google Sheets SMS Bot

This project allows you to setup an SMS bot to get information from your Google Sheets. It uses Google Authentication, Google Sheets API, and the Twilio Messaging API.

## Google API Setup

### Authentication

- In order to authenticate with your Google API account, a service account is needed.
  Follow the steps here to create one: <https://cloud.google.com/iam/docs/creating-managing-service-accounts>
- Once your service account has been created, create an account key: <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating>
- Once created, download the json file. You will need to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of this file.

### Setup Permissions for Google Sheets

- In order for your Google Service Account to be able to access your Google Sheets, you will need to explicitly grant it permissions. From your Google Cloud dashboard, get your service account email and share your Google Sheet with that email address.

### Google Sheets Configuration

The Google Sheets configuration that is being used here allows for multiple Google Sheets to be accessed,
and allows for SMS messages to be customized for each Google Sheet. Below is an example json snippet which
shows you how to customize your own message request, response, and sheet data. More information on how to
use Google Sheet ranges can be found here: <https://developers.google.com/sheets/api/guides/concepts#cell>

Example:

```json
{
    "spreadsheets": 
    [
        {
            "spreadsheet_id": "abcdefghijklmnopqrstuvwxyz0123456789",
            "spreadsheet_ranges": [
                {
                    "request_message": "checking balance",
                    "response_message": "Current checking balance",
                    "range": "Sheet1!A1"
                }
            ]
        }
    ]
}
```

## Twilio Setup

- Setup Twilio Account: <https://www.twilio.com/docs/sms/quickstart/python>

## Load Environment Variables`

There are several environment variables that you will need to load. Some are Flask specific, Google specific, and Twilio specific. 

Create an `.env` file at the root directory of this repository. This is where you will place your environment variables. This application will load those variables into your environment.

| Variable | Value |
| -------- | ----- |
| SCOPES | |
| GOOGLE_APPLICATION_CREDENTIALS | |



Example:

```
FLASK_APP=app
FLASK_ENV=development

SCOPES=https://www.googleapis.com/auth/spreadsheets
GOOGLE_APPLICATION_CREDENTIALS=<path to GOOGLE_APPLICATION_CREDENTIALS json file>

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_API_KEY=
TWILIO_PHONE_NUMBER=+11234567890
PHONE_NUMBERS=+11234567890,+11234567890
TWILIO_SERVICE_SID=
TWILIO_CONVERSATION_SID=
TWILIO_MESSAGING_SERVICE_SID=
```
