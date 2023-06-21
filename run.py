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
SHEET = GSPREAD_CLIENT.open('RSVP_Responses').worksheet('Responses')


def main_menu():
    """
    Main menu
    """
    print('Main Menu\n')
    print('1. RSVP Response Data Analysis')
    print('2. Question/Comment Manager\n')
    print("Select an option by entering 1 or 2\n")
    
    while True:
        selection = input("Enter your choice here and press enter to continue:\n")
        if validate_menu_selection(selection):
            if selection == '1':
                analysis()
            elif selection == '2':
                print('manage questions')
            break


def validate_menu_selection(selection):
    """
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    try:
        selection = int(selection)
        if selection > 2:
            raise ValueError(
                f"Please enter 1 or 2, you entered {selection}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def responses_total_calc(col):
    """
    Calculate the total number of rows of data in the worksheet.
    """
    total_rows = len(SHEET.col_values(col)[1:])
    blank_rows = SHEET.col_values(col).count("")
    responses = total_rows - blank_rows
    return responses


def question_responses(col):
    possible_answers = set((SHEET.col_values(col)[1:]))
    while "" in possible_answers:
        possible_answers.remove("")
    all_column_values = list((SHEET.col_values(col)[1:]))
    total_responses = responses_total_calc(col)
    for answer in possible_answers:
        answer_percent = (all_column_values.count(answer)/total_responses)*100
        print(f"{answer} = {answer_percent}%")


def calc_attendance_number():
    attendance_answers = SHEET.col_values(5)[1:]
    while "" in attendance_answers:
        attendance_answers.remove("")
    attendance_int = [int(answer) for answer in attendance_answers]
    total = sum(attendance_int)
    print(f"There are a total of {total} expected attendees.")


def analysis():
    """
    Run all analysis functions.
    """
    responses_total = responses_total_calc(1)
    print(f'The invitation received a total of {responses_total} responses.\n')
    question_responses(4)
    calc_attendance_number()
    question_responses(6)


print('Welcome to the RSVP Response Manager.\n')
main_menu()
