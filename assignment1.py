#!/usr/bin/env python3
'''
OPS445 Assignment 1
Program: assignment1.py
Author: Abdul Mostofa
Seneca ID: amostofa
Semester: Summer 2026

The python code in this file (assignment1.py) is original work written by
Abdul Mostofa. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''

import sys


def day_of_week(year: int, month: int, date: int) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + date) % 7
    return days[num]


def leap_year(year: int) -> bool:
    '''
    Return True if the given year is a leap year, False otherwise.
    A year is a leap year if divisible by 4, except century years
    must also be divisible by 400.
    '''
    if year % 400 == 0:
        return True    # divisible by 400: always a leap year
    if year % 100 == 0:
        return False   # divisible by 100 but not 400: not a leap year
    if year % 4 == 0:
        return True    # divisible by 4 but not 100: leap year
    return False       # not divisible by 4: not a leap year


def mon_max(month: int, year: int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
    # February's days depend on whether it's a leap year
    feb_days = 29 if leap_year(year) else 28

    # Map each month number to its maximum number of days
    month_days = {
        1: 31, 2: feb_days, 3: 31, 4: 30,
        5: 31, 6: 30,  7: 31, 8: 31,
        9: 30, 10: 31, 11: 30, 12: 31
    }
    return month_days[month]


def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This function has been tested to work for year after 1582
    '''
    # Split the date string into year, month, day components
    str_year, str_month, str_day = date.split('-')

    # Convert string components to integers for arithmetic
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    # Advance to the next day by adding 1
    tmp_day = day + 1

    # Use mon_max() instead of duplicating leap-year logic here
    if tmp_day > mon_max(month, year):
        # We've passed the last day of the month: wrap to day 1 of next month
        to_day = tmp_day % mon_max(month, year)
        tmp_month = month + 1
    else:
        # Still within the same month
        to_day = tmp_day
        tmp_month = month

    # Check if we've gone past December into a new year
    if tmp_month > 12:
        to_month = 1        # reset to January
        year = year + 1     # increment the year
    else:
        to_month = tmp_month

    # Format the next date as a zero-padded YYYY-MM-DD string
    next_date = f"{year}-{to_month:02}-{to_day:02}"
    return next_date


def usage():
    "Print a usage message to the user and exit"
    print('Usage: assignment1.py YYYY-MM-DD YYYY-MM-DD')
    sys.exit(1)


def valid_date(date: str) -> bool:
    "check validity of date and return True if valid"
    # Date string must be exactly 10 characters long (YYYY-MM-DD)
    if len(date) != 10:
        return False

    # Hyphens must be in positions 4 and 7
    if date[4] != '-' or date[7] != '-':
        return False

    # Split into parts and confirm all three segments are present
    parts = date.split('-')
    if len(parts) != 3:
        return False

    # Each segment must contain only digits
    if not (parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit()):
        return False

    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])

    # Month must be between 1 and 12 inclusive
    if month < 1 or month > 12:
        return False

    # Day must be at least 1 and no more than the month allows (handles leap years)
    if day < 1 or day > mon_max(month, year):
        return False

    return True


def day_count(start_date: str, stop_date: str) -> int:
    "Loops through range of dates, and returns number of weekend days"
    weekend_count = 0
    current_date = start_date

    # Walk forward one day at a time from start_date to stop_date (inclusive)
    while current_date <= stop_date:
        # Parse the current date into components for day_of_week()
        str_year, str_month, str_day = current_date.split('-')
        dow = day_of_week(int(str_year), int(str_month), int(str_day))

        # Count Saturdays and Sundays
        if dow in ('sat', 'sun'):
            weekend_count += 1

        # Advance to the next day
        current_date = after(current_date)

    return weekend_count


if __name__ == "__main__":
    # Verify that exactly two arguments were provided (besides the script name)
    if len(sys.argv) != 3:
        usage()

    date1 = sys.argv[1]
    date2 = sys.argv[2]

    # Both arguments must be valid dates; print usage and exit if not
    if not valid_date(date1) or not valid_date(date2):
        usage()

    # Always use the earlier date as start and the later as end,
    # regardless of the order the user entered them —
    # reversing them would cause day_count() to loop forever
    if date1 <= date2:
        start_date = date1
        end_date = date2
    else:
        start_date = date2
        end_date = date1

    # Calculate and display the result
    count = day_count(start_date, end_date)
    print(f'The period between {start_date} and {end_date} includes {count} weekend days.')
