import gspread
import itertools
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
        selection = input("Enter your choice here"
                          " and press enter to continue:\n")
        if validate_menu_selection(selection):
            if selection == '1':
                analysis()
            elif selection == '2':
                question_manager()
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
    input("Press the Enter key to return to the main menu.")
    main_menu()


def email_response():
    print('email response')


def ignore_question(row_data):
    print('Are you sure you want to process this question as "ignored"?')
    ignore = input('Enter Y or N and press enter to continue:').strip()
    while True:
        if ignore == 'Y' or 'y':
            row_num = row_data['row']
            SHEET.update_cell(row_num, 8, 'Ignored')
        elif ignore == 'N' or 'n':
            print('Returning to question/comment processing menu')
            question_processing_menu(row_data)
        break


def skip_question():
    print('skip')


def question_processing_menu(row):
    print(
        "Review the question/comment recieved "
        "and choose an appropriate action\n"
    )
    print("To respond to the question/comment enter 1")
    print("To mark the question/comment as ignored enter 2")
    print(
        "To skip to the next question/comment "
        "without processing enter 3"
    )
    print("To exit to the main menu enter 4\n")
    print("Press enter to continue\n")
    while True:
        action_selection = input("Enter a number between 1 and 4 here:\n")

        if validate_data(action_selection):
            if action_selection == '1':
                email_response()
            elif action_selection == '2':
                ignore_question(row)
            elif action_selection == '3':
                skip_question()
            elif action_selection == '4':
                print('Exiting to main menu...')
                main_menu()
            break


def validate_data(value):
    """
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    try:
        selection = int(value)
        if selection > 4 or selection < 1:
            raise ValueError(
                f"Please enter a number from 1 - 4, you entered {value}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def question_asked():
    """
    Create a list of responses with questions or comments
    that have not been responded to or ignored,
    as dictionaries with headings as key and data as value.
    """
    data_vals = SHEET.get_all_values()
    headings = data_vals[0]
    headings.insert(0, 'row')
    del data_vals[0]
    headings_vals_dicts = []
    row_num = 2
    for row in data_vals:
        row.insert(0, row_num)
        row_num += 1
        zipped = dict(zip(headings, row))
        headings_vals_dicts.append(zipped)

    asked_question = [
        row for row in headings_vals_dicts if not (
            row["Comments/questions"] == ""
        ) and not (
            row["Responded/ignored"] == "Responded"
        ) and not (
            row["Responded/ignored"] == "Ignored"
        )
    ]
    return asked_question


def view_questions(data):
    """
    Check if list contains any response data items,
    iterate through the list, print the response data
    and run function to process question/comment or
    print a message informing the user that there are
    no questions/comments to review.
    """
    if len(data) >= 1:
        for row in data:
            top_of_list = dict(itertools.islice(row.items(), 0, 8))
            for key in top_of_list:
                print(f"{key}: {top_of_list[key]}")
            print('\n')
            question_processing_menu(row)
        print('No more questions.')
        print('You have reached the end of the list.')
        input("Press the Enter key to return to the main menu.")
    else:
        print('There are currently no questions/comments to review.')
        input("Press the Enter key to return to the main menu.")
        main_menu()


def question_manager():
    question_rows = question_asked()
    view_questions(question_rows)


print('Welcome to the RSVP Response Manager.\n')
main_menu()
