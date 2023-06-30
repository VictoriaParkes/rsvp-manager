import gspread
from google.oauth2.service_account import Credentials
import sys
import itertools
import configparser
import datetime
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


try:
    SHEET = GSPREAD_CLIENT.open('RSVP_Responses').worksheet('Responses')
except Exception:
    print(f'Sorry, the RSVP worksheet can not be loaded.')


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


def transition_between_screens(text):
    clear()
    print(text)
    pause()
    clear()


def main_menu():
    """
    Main menu
    """
    print('Main Menu\n')
    print('1. RSVP Response Data Analysis')
    print('2. Question/Comment Manager')
    print('3. Exit RSVP Response Manager\n')
    print('Select an option by entering a number between 1 and 3.\n')
    while True:
        selection = input('Enter your choice here'
                          ' and press enter to continue:\n').strip()
        if validate_numerical_input(3, selection):
            if selection == '1':
                transition_between_screens('Analysing data...')
                analysis()
            elif selection == '2':
                transition_between_screens('Opening Question/Comment '
                                           'Manager...')
                question_manager()
            elif selection == '3':
                clear()
                sys.exit('Goodbye')
            break


def validate_numerical_input(input_count, value):
    """
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    REWRITE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    try:
        selection = int(value)
        if selection > input_count or selection < 1:
            raise ValueError(
                f'Please enter a number from 1 - {input_count}, '
                f'you entered {value}'
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
    blank_rows = SHEET.col_values(col).count('')
    responses = total_rows - blank_rows
    return responses


def question_responses(col):
    question = SHEET.col_values(col)[0]
    possible_answers = set((SHEET.col_values(col)[1:]))
    print(f'Analysis of answer to question "{question}":')
    while '' in possible_answers:
        possible_answers.remove('')
    all_column_values = list((SHEET.col_values(col)[1:]))
    total_responses = responses_total_calc(col)
    for answer in possible_answers:
        answer_percent = (all_column_values.count(answer)/total_responses)*100
        print(f'>>> {answer_percent}% of the respondents answered {answer}.')


def calc_attendance_number():
    attendance_answers = SHEET.col_values(5)[1:]
    while '' in attendance_answers:
        attendance_answers.remove('')
    attendance_int = [int(answer) for answer in attendance_answers]
    total = sum(attendance_int)
    print(f'\nThere are a total of {total} expected attendees.\n')


def analysis():
    """
    Run all analysis functions.
    """
    responses_total = responses_total_calc(1)
    print(f'The invitation received a total of {responses_total} responses.\n')
    question_responses(4)
    calc_attendance_number()
    question_responses(6)
    input('\nPress the Enter key to return to the main menu.')
    transition_between_screens('Returning to main menu...')
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


def compose_email_screen(row_data, name, email_address, greeting):
    display_row_data(row_data)
    print(f'Compose email message to {name} at {email_address}\n')
    compose_email_instructions()
    print(greeting)


def update_email_composition(row_data,
                             name,
                             email_address,
                             greeting,
                             input_list):
    clear()
    compose_email_screen(row_data, name, email_address, greeting)
    print(''.join(input_list))
    print('\033[2A')


def compose_email_message(row_data, name, email_address):
    greeting = f'Hi {name},\n'
    sign_off = 'Kind regards,\nRSVP Team'
    compose_email_screen(row_data, name, email_address, greeting)
    input_list = []
    while True:
        break_flag = False
        user_input = input().strip()
        if user_input == 'end message':
            clear()
            print('Please review you email message before continuing...\n')
            print(greeting)
            print(''.join(input_list))
            print(f'{sign_off}\n')
            print('Confirm if this message is complete to send email.')
            while True:
                confirm = input('Enter Y or N and '
                                'press enter to continue:').strip().lower()
                if confirm == 'y':
                    break_flag = True
                    break
                elif confirm == 'n':
                    update_email_composition(row_data,
                                             name,
                                             email_address,
                                             greeting,
                                             input_list)
                    break
                else:
                    print('\033[2A')
                    print('Enter Y for yes or N for no                 ')
            if break_flag:
                break
        elif user_input == '':
            input_list.append('\n')
        elif user_input == 'delete last line':
            if len(input_list) > 0:
                del input_list[-1]
                update_email_composition(row_data,
                                         name,
                                         email_address,
                                         greeting,
                                         input_list)
            else:
                update_email_composition(row_data,
                                         name,
                                         email_address,
                                         greeting,
                                         input_list)
        elif user_input == 'delete message':
            input_list.clear()
            update_email_composition(row_data,
                                     name,
                                     email_address,
                                     greeting,
                                     input_list)
        elif user_input == 'exit':
            transition_between_screens('Returing to question/comment '
                                       'processing menu...')
            question_processing_menu(row_data)
        else:
            input_list.append(user_input + '\n')
    input_list.insert(0, greeting + '\n')
    input_list.append('\n' + sign_off)
    message = ''.join(input_list)
    return message


def convert_date(date_time):
    # The format
    format = '%a, %d %b %Y %H:%M:%S %Z'
    datetime_str = datetime.datetime.strptime(date_time, format)
    format_datetime_str = datetime_str.strftime("%d/%m/%Y %H:%M:%S")
    return format_datetime_str


def send_email(row_data, name, email_address, message):
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
                return date
            except Exception as e:
                print(f'Sorry an error has occurred: {e}')
    try:
        settings = CONFIG["SETTINGS"]
    except Exception:
        settings = {}
    API = settings.get("APIKEY", None)
    from_email = settings.get("FROM", None)
    to_emails = row_data['Email address']
    subject = "RSVP Question/Comment Response"
    html_content = message
    date = sendMailUsingSendGrid(API,
                                 from_email,
                                 to_emails,
                                 subject,
                                 html_content)
    print(f'Email successfully sent to {name} at {email_address}\n')
    timestamp = convert_date(date)
    row_num = row_data['row']
    print('Updating worksheet...')
    pause()
    SHEET.update_cell(row_num, 8, 'Responded')
    SHEET.update_cell(row_num, 9, timestamp)
    SHEET.update_cell(row_num, 10, message)
    print('Worksheet successfully updated\n')


def email_response(row_data):
    name = row_data['Name']
    email_address = row_data['Email address']
    message = compose_email_message(row_data, name, email_address)
    clear()
    print(f'Sending email to {name} at {email_address}...')
    pause()
    send_email(row_data, name, email_address, message)
    input('Press enter to continue...')


def ignore_question(row_data):
    display_row_data(row_data)
    print('Are you sure you want to process this question as "ignored"?')
    while True:
        ignore = input('Enter Y or N and press enter to continue:').strip().lower()
        if ignore == 'y':
            clear()
            print('Marking question/comment as ignored in worksheet...')
            row_num = row_data['row']
            SHEET.update_cell(row_num, 8, 'Ignored')
            pause()
            transition_between_screens('Worksheet updated, returning '
                                       'to Question/Comment Manager...')
            break
        elif ignore == 'n':
            transition_between_screens('Returning to question/comment '
                                       'processing menu...')
            question_processing_menu(row_data)
        else:
            print('\033[2A')
            print('Enter Y for yes or N for no                    ')


def skip_question(row_data):
    display_row_data(row_data)
    print('If you choose to skip this question it will still be available '
          'to process later.')
    print('Are you sure you want to skip this question for now?')
    while True:
        skip = input('Enter Y or N and press enter to continue:').strip().lower()
        if skip == 'y':
            transition_between_screens('Question/comment skipped, returning '
                                       'to question/comment manager…')
            break
        elif skip == 'n':
            transition_between_screens('Returning to question/comment '
                                       'processing menu…')
            question_processing_menu(row_data)
        else:
            print('\033[2A')
            print('Enter Y for yes or N for no.                    ')


def display_row_data(row):
    top_of_list = dict(itertools.islice(row.items(), 1, 8))
    for key in top_of_list:
        print(f"{key}: {top_of_list[key]}")
    print('\n')


def question_processing_menu(row):
    print('Question/Comment Manager\n')
    print(
        "Review the question/comment recieved "
        "and choose an appropriate action\n"
    )
    display_row_data(row)
    print('1. Respond to the question/comment')
    print('2. Mark the question/comment as ignored')
    print('3. Skip to the next question/comment')
    print('4. Exit to the main menu\n')
    while True:
        selection = input('Enter your choice here'
                          ' and press enter to continue:\n').strip()
        if validate_numerical_input(4, selection):
            if selection == '1':
                transition_between_screens('Opening Email Composer...')
                email_response(row)
            elif selection == '2':
                clear()
                ignore_question(row)
            elif selection == '3':
                clear()
                skip_question(row)
            elif selection == '4':
                transition_between_screens('Exiting to main menu...')
                main_menu()
            break


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
        transition_between_screens('Returning to main menu...')
        main_menu()
    else:
        print('There are currently no questions/comments to review.')
        input("Press the Enter key to return to the main menu.")
        transition_between_screens('Returning to main menu...')
        main_menu()


def question_manager():
    question_rows = question_asked()
    view_questions(question_rows)


if __name__ == "__main__":
    print('Welcome to the RSVP Response Manager.\n')
    main_menu()
