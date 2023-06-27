import datetime


# Function to convert string to datetime
def convert_date(date_time):
    # The format
    format = '%a, %d %b %Y %H:%M:%S %Z'
    datetime_str = datetime.datetime.strptime(date_time, format)
    format_datetime_str = datetime_str.strftime("%d/%m/%Y %H:%M:%S")

    return format_datetime_str


# Driver code
date_time = 'Tue, 27 Jun 2023 16:22:18 GMT'
print(convert(date_time))
print(type(convert(date_time)))
