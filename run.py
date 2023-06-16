import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('RSVP_Responses')

""" Add variable for worksheet """
responses_worksheet = SHEET.worksheet('Responses')

def responses_total():
    """
    Calculate the total number of rows of data in the worksheet.
    """
    total_rows = len(responses_worksheet.col_values(4)[1:])
    blank_rows = responses_worksheet.col_values(4).count("")
    responses = total_rows - blank_rows
    print(f'The invitation received a total of {responses} responses.')


def analysis():
    """
    Run all analysis functions.
    """
    responses_total()


analysis()
