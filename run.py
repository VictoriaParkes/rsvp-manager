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


def responses_total_calc(col):
    """
    Calculate the total number of rows of data in the worksheet.
    """
    total_rows = len(responses_worksheet.col_values(col)[1:])
    blank_rows = responses_worksheet.col_values(col).count("")
    responses = total_rows - blank_rows
    return responses


def question_responses(col):
    possible_answers = set((responses_worksheet.col_values(col)[1:]))
    possible_answers.remove("")
    all_column_values = list((responses_worksheet.col_values(col)[1:]))
    total_responses = responses_total_calc(col)
    for answer in possible_answers:
        answer_percent = (all_column_values.count(answer)/total_responses)*100
        print(f"{answer} = {answer_percent}%")


def analysis():
    """
    Run all analysis functions.
    """
    responses_total = responses_total_calc(1)
    print(f'The invitation received a total of {responses_total} responses.')
    question_responses(4)
    question_responses(6)


analysis()
