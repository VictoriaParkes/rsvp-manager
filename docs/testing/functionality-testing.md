[Back to README.md](../../README.md#functionality-testing)

# Functionality Testing

| Test Label | Test Action | Expected Outcome | Test Outcome |
|----------|-----------|----------------|------------|
| Worksheet check - Success | Run program | Welcome message and main menu are displayed. | PASS |
| Worksheet check - Exception | Rename worksheet and run program | Message 'Sorry, the RSVP worksheet cannot be loaded.' is displayed in the terminal. User is asked to press Enter key to exit the program after which the message 'Goodbye' is displayed and the program is closed. | PASS |
| Welcome Message | Run program | Welcome message is displayed at top of screen. | PASS |
| Main menu | Run program | Main menu is displayed below welcome message. | PASS |
| Main Menu - input validation | Enter invalid inputs | Exception raised, error message displayed and user asked for valid input. | PASS |
| Main Menu - option 1. RSVP Response Data Analysis | Enter 1 in input for main menu | Data analysis is displayed. | PASS |
| Main Menu - option 2. Question/Comment Manager | Enter 2 in input for main menu | Question/Comment Manager screen is displayed. | PASS |
| Main Menu - option 3. Exit RSVP Response Manager | Enter 3 in input for main menu | Message 'Goodbye' is displayed and program is closed. | PASS |
| Data analysis | Enter 1 in input for main menu | The total number of responses is displayed. The percentage of attending and not attending answers given is displayed. The total number of expected attendees is displayed. The percentage of answers to how respondents heard about the event is displayed. The user is asked to press enter to return to main menu. | PASS |
| Data analysis - return to main menu | Press enter when data analysis page is displayed | The program returns to the main menu. | PASS |
| Question/Comment Manager | Enter 2 in input for main menu | The Question/Comment Manager screen is displayed. The user is asked to review the question/comment and choose an action. The first row of data in the worksheet that has a value for question/comment and no value for responded/ignored is displayed. The question/comment processing menu is displayed and the user is asked to enter the number of the option they wish to proceed with. | PASS |
| Question/Comment Processing Menu - input validation | Enter invalid inputs | Exception raised, error message displayed and user asked for valid input. | PASS |
| Question/Comment Processing Menu - option 1. Respond to the question/comment | Enter 1 in input for Question/Comment Processing Menu | The email composer screen is displayed. | PASS |
| Question/Comment Processing Menu - option 2. Mark the question/comment as ignored | Enter 2 in input for Question/Comment Processing Menu | The ignore question/comment screen is displayed. | PASS |
| Question/Comment Processing Menu - option 3. Skip to the next question/comment | Enter 3 in input for Question/Comment Processing Menu | The skip question/comment screen is displayed. | PASS |
| Question/Comment Processing Menu - option 4. Exit to the main menu | Enter 4 in input for Question/Comment Processing Menu | The user is returned to the main menu. | PASS |
| Email composer screen | Enter 1 in input for Question/Comment Processing Menu | The row data is displayed at the top of the screen. The user is asked to compose a message in response to the question/comment. The message composer instructions are displayed. The email greeting is displayed and the user is presented with an input field in which to enter their message and commands. | PASS |
| Email composer input - not defined command | Enter any text into email composer input except a defined command | User input is displayed and they are able to continue entering lines for their message. | PASS |
| Email composer input - 'delete last line' | Enter 'delete last line' into email composer input | The last line entered is deleted and the user is able to continue entering lines for their message. | PASS |
| Email composer input - 'delete message' | Enter 'delete message' into email composer input | The lines entered by the user are deleted and they are able to start composing their message again. | PASS |
| Email composer input - 'exit' | Enter 'exit' into email composer input | The program returns to the question processing menu. | PASS |
| Email composer input - 'end message' | Enter 'end message' into email composer input | The user is asked to review their message and enter Y or N to confirm if the message is complete and send the message. | PASS |
| Confirm message complete - Y input | Enter Y into the confirm message complete input | The message is sent to the respondent via email, the worksheet is updated with the value 'Responded' in the Responded/ignored column, the timestamp for when the email was sent in the 'Question response timestamp' column and the message in the 'Response to question' column of the row containing the processed question.	The user is asked to press the enter key to continue after which they are returned to the Question/comment manager where the next row of data in the worksheet that has a value for question/comment and no value for responded/ignored is displayed. | PASS |
| Confirm message complete - N input | Enter N into the confirm message complete input | The program returns to the email composer screen and the user is able to continue composing their message. | PASS |
| Confirm message complete - invalid input | Enter invalid value into the confirm message complete input | The user is informed to enter Y for yes or N for no into the input. | PASS |
| Ignore question/comment screen | Enter 2 in input for Question/Comment Processing Menu | The row data is displayed at the top of the screen. The user is asked to confirm if they wish to mark the question/comment as ignored by entering Y or N into the input. | PASS |
| Ignore question/comment - Y input | Enter Y into the ignore confirmation input | The worksheet is updated with the value "Ignored" in the "Responded/ignored" column of the row containing the processed question. The user is returned to the Question/comment manager where the next row of data in the worksheet that has a value for question/comment and no value for responded/ignored is displayed. | PASS |
| Ignore question/comment - N input | Enter N into the ignore confirmation input | The user is returned to the Question/Comment Processing Menu. | PASS |
| Ignore question/comment - invalid input | Enter value other than Y or N into the ignore confirmation input | The user is asked to enter Y for yes or N for no into the input. | PASS |
| Skip question/comment screen | Enter 3 in input for Question/Comment Processing Menu | The row data is displayed at the top of the screen. The user is asked to confirm if they wish to skip this question/comment by entering Y or N into the input. | PASS |
| Skip question/comment - Y input | Enter Y into the skip confirmation input | The user is returned to the Question/comment manager where the next row of data in the worksheet that has a value for question/comment and no value for responded/ignored is displayed. | PASS |
| Skip question/comment - N input | Enter N into the skip confirmation input | 	The user is returned to the Question/Comment Processing Menu. | PASS |
| Skip question/comment - invalid input | Enter value other than Y or N into the skip confirmation input | The user is asked to enter Y for yes or N for no into the input. | PASS |

[Back to README.md](../../README.md#functionality-testing)
