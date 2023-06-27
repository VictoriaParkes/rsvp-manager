import gspread
from google.oauth2.service_account import Credentials
import itertools
import configparser
import datetime
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('RSVP_Responses').worksheet('Responses')
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


def clear():
    """
    Clear the screen
    """
    print('\033c')


def pause():
    """
    Pause the program
    """
    time.sleep(2)


# def transition_between_screens():


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
                clear()
                print('Analysing data...')
                pause()
                clear()
                analysis()
            elif selection == '2':
                clear()
                print('Opening Question/Comment Manager...')
                pause()
                clear()
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
    clear()
    print('Returning to main menu...')
    pause()
    clear()
    main_menu()


def compose_email_instructions():
    print('Instructions')
    print('- Enter the main body of your message into the terminal, '
          'the greeting and sign off are automatically added for you.')
    print('- Press the enter key to submit each line and start a new line.')
    print('- Type "delete last line" and press enter to delete the last '
          'line entered and continue composing the message.')
    print('- Type "delete message" and press enter to delete the whole '
          'message and start again.')
    print('- Type "end message" and press enter to finish composing the '
          'message.\n')


def update_email_composition(name, greeting, comment_question, input_list):
    clear()
    compose_email_instructions()
    print(f'The question/comment left by {name} was:')
    print(comment_question)
    print(greeting)
    print(''.join(input_list))
    print('\033[2A')


def compose_email_message(row_data):
    name = row_data['Name']
    email_address = row_data['Email address']
    comment_question = row_data['Comments/questions']
    greeting = f'Hi {name},\n'
    sign_off = '\nKind regards,\nRSVP Team'
    print(f'Compose email message to {name} at {email_address}\n')
    compose_email_instructions()
    print(f'The question/comment left by {name} was:')
    print(f'{comment_question}\n')
    input_list = []
    print(greeting)
    while True:
        user_input = input().strip()
        if user_input.lower() == 'end message':
            # add greeting and sign off, review question
            # confirm message complete y/n
            print('\033c')
            break
        elif user_input == '':
            input_list.append('\n')
        elif user_input.lower() == 'delete last line':
            del input_list[-1]
            update_email_composition(name,
                                     greeting,
                                     comment_question,
                                     input_list)
        elif user_input.lower() == 'delete message':
            input_list.clear()
            update_email_composition(name,
                                     greeting,
                                     comment_question,
                                     input_list)
        elif user_input.lower() == 'exit':
            clear()
            print('Returing to question/comment processing menu...')
            pause()
            clear()
            question_processing_menu(row_data)
        else:
            input_list.append(user_input + '\n')
    input_list.insert(0, greeting + '\n')
    input_list.append(sign_off)
    message = ''.join(input_list)
    return message


def convert_date(date_time):
    # The format
    format = '%a, %d %b %Y %H:%M:%S %Z'
    datetime_str = datetime.datetime.strptime(date_time, format)
    format_datetime_str = datetime_str.strftime("%d/%m/%Y %H:%M:%S")
    return format_datetime_str


def send_email(row_data, message):
    def sendMailUsingSendGrid(
        API,
        from_email,
        to_emails,
        subject,
        html_content
    ):
        if (
            API is not None
            and from_email is not None
            and to_emails is not None
        ):
            email = Mail(from_email, to_emails, subject, html_content)
            try:
                sg = SendGridAPIClient(API)
                response = sg.send(email)
                date = response.headers['Date']
                timestamp = convert_date(date)
                print('\nEmail sent')
                row_num = row_data['row']
                SHEET.update_cell(row_num, 8, 'Responded')
                SHEET.update_cell(row_num, 9, timestamp)
                SHEET.update_cell(row_num, 10, message)
            except Exception as e:
                print(e)
    try:
        settings = CONFIG["SETTINGS"]
    except Exception:
        settings = {}
    API = settings.get("APIKEY", None)
    from_email = settings.get("FROM", None)
    to_emails = row_data['Email address']
    subject = "RSVP Question/Comment Response"
    html_content = message
    sendMailUsingSendGrid(API, from_email, to_emails, subject, html_content)


def email_response(row_data):
    message = compose_email_message(row_data)
    print(message)
    # send_email(row_data, message)


def ignore_question(row_data):
    print('Are you sure you want to process this question as "ignored"?')
    ignore = input('Enter Y or N and press enter to continue:').strip()
    while True:
        if ignore.lower() == 'y':
            clear()
            print('Marking question/comment as ignored in worksheet...')
            row_num = row_data['row']
            SHEET.update_cell(row_num, 8, 'Ignored')
            pause()
            clear()
            print('Worksheet updated, '
                  'returning to Question/Comment Manager...')
            pause()
            clear()
        elif ignore.lower() == 'n':
            clear()
            print('Returning to question/comment processing menu...')
            pause()
            clear()
            question_processing_menu(row_data)
        break


def skip_question(row):
    skip = input('Enter Y or N and press enter to continue:').strip()
    while True:
        if skip.lower() == 'y':
            clear()
            print('Question/comment skipped, '
                  'returning to question/comment manager…')
            pause()
            clear()
        elif skip.lower() == 'n':
            clear()
            print('Returning to question/comment processing menu…')
            pause()
            clear()
            question_processing_menu(row)
        break


def display_row_data(row):
    top_of_list = dict(itertools.islice(row.items(), 1, 8))
    for key in top_of_list:
        print(f"{key}: {top_of_list[key]}")
    print('\n')


def question_processing_menu(row):
    print(
        "Review the question/comment recieved "
        "and choose an appropriate action\n"
    )
    display_row_data(row)
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
                clear()
                print('Opening Email Composer...')
                pause()
                clear()
                email_response(row)
            elif action_selection == '2':
                ignore_question(row)
            elif action_selection == '3':
                skip_question(row)
            elif action_selection == '4':
                clear()
                print('Exiting to main menu...')
                pause()
                clear()
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
            question_processing_menu(row)
        print('No more questions.')
        print('You have reached the end of the list.')
        input("Press the Enter key to return to the main menu.")
        clear()
        print('Returning to main menu...')
        pause()
        clear()
        main_menu()
    else:
        print('There are currently no questions/comments to review.')
        input("Press the Enter key to return to the main menu.")
        clear()
        print('Returning to main menu...')
        pause()
        clear()
        main_menu()


def question_manager():
    question_rows = question_asked()
    view_questions(question_rows)


print('Welcome to the RSVP Response Manager.\n')
main_menu()
