#! /usr/bin/env python3
'''
 Program:
    Name: Andrew Dixon            File: dateDeterminator.py
    Date: Wed Aug 10 2022
   Notes:

    PyDateConverter - Handy date information and conversion to common formats.
    Copyright (C) 2023  Andrew Dixon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3..
'''

import re


RE_ISO_DATE = re.compile(r'\b([0-9]{4})[-/.]?([01][0-9])[-/.]?([0-3][0-9])\b')
RE_USA_DATE = re.compile(r'\b([01][0-9])[-/.]?([0-3][0-9])[-/.]?([0-9]{4})\b')
RE_EUR_DATE = re.compile(r'\b([0-3][0-9])[-/.]?([0-1][0-9])[-/.]?([0-9]{4})\b')
RE_LJUL_DATE = re.compile(r'\b([0-9]{4})[-/.]?([0-3][0-9][0-9])\b')
RE_MDY_DATE = re.compile(r'\b([0-1][0-9])[-/.]?([0-3][0-9])[-/.]?([0-9]{2})\b')
RE_YMD_DATE = re.compile(r'\b([0-9]{2})[-/.]?([0-1][0-9])[-/.]?([0-3][0-9])\b')
RE_DMY_DATE = re.compile(r'\b([0-3][0-9])[-/.]?([0-1][0-9])[-/.]?([0-9]{2})\b')
RE_JUL_DATE = re.compile(r'\b([0-9]{2})[-/.]?([0-3][0-9][0-9])\b')
SEPARATORS = frozenset(".-/")


def main():
    # Make this loop forever. Leave by putting a q/Q on the input line.
  while True:
    # Get the information from the user.
    inDate = input("Date to check ((Q)uit): ")

    # Make it so that we can get out of our loop.
    if inDate.strip().upper().startswith("Q"):
      return

    rc = guessDateFormat(inDate)

    # Print the output and if it was a numeric value or not.
    print("\nDate:> {}\n".format(rc))


def guessDateFormat(tstDate: str) -> list:
  rtnVal = []

  if len(tstDate) in range(8, 11):
    m = RE_ISO_DATE.match(tstDate)      # Valid: YYYY-MM-DD / YYYYMMDD
    if m is not None:
      if int(m[2]) in range(1, 13) and validDom(int(m[2]), int(m[3]), int(m[1])) and validSep(tstDate):
        rtnVal.append('ISO')

    m = RE_USA_DATE.match(tstDate)      # Valid: MM-DD-YYYY / MMDDYYYY
    if m is not None:
      if int(m[1]) in range(1, 13) and validDom(int(m[1]), int(m[2]), int(m[3])) and validSep(tstDate):
        rtnVal.append('USA')

    m = RE_EUR_DATE.match(tstDate)      # Valid: DD-MM-YYYY / DDMMYYYY
    if m is not None:
      if int(m[2]) in range(1, 13) and validDom(int(m[2]), int(m[1]), int(m[3])) and validSep(tstDate):
        rtnVal.append('EUR')

  if len(tstDate) in range(7, 9):
    m = RE_LJUL_DATE.match(tstDate)     # Valid: YYYY-DDD / YYYYDDD

    if m is not None:
      if leapYear(int(m[1])):
        daysInYear = 366

      else:
        daysInYear = 365

      if int(m[2]) in range(1, daysInYear + 1):
        rtnVal.append('LJUL')

  if len(tstDate) in range(6, 9):
    m = RE_MDY_DATE.match(tstDate)      # Valid: MM-DD-YY / MMDDYY
    if m is not None:
      if int(m[1]) in range(1, 13) and validDom(int(m[1]), int(m[2])) and validSep(tstDate):
        rtnVal.append('MDY')

    m = RE_YMD_DATE.match(tstDate)      # Valid: YY-MM-DD / YYMMDD
    if m is not None:
      if int(m[2]) in range(1, 13) and validDom(int(m[2]), int(m[3])) and validSep(tstDate):
        rtnVal.append('YMD')

    m = RE_DMY_DATE.match(tstDate)      # Valid: DD-MM-YY / DDMMYY
    if m is not None:
      if int(m[2]) in range(1, 13) and validDom(int(m[2]), int(m[1])) and validSep(tstDate):
        rtnVal.append('DMY')

  if len(tstDate) in range(5, 7):
    m = RE_JUL_DATE.match(tstDate)      # Valid: YY-DDD / YYDDD
    if m is not None:
      if int(m[2]) in range(1, 367):
        rtnVal.append('JUL')

  return rtnVal


def leapYear(year: int) -> bool:
  ''' Determine if a given year is a leap year '''
  return ((year % 400 == 0) or ((year % 100 != 0) and (year % 4 == 0)))


def validDom(month: int, day: int, year=None) -> bool:
  ''' Determine if day of month is valid for a given month '''
  thirtyOne = [1, 3, 5, 7, 8, 10, 12]
  thirty = [4, 6, 9, 11]

  # Deal with February
  if year and month == 2:
    if leapYear(int(year)):
      validMaxDom = 29

    else:
      validMaxDom = 28

  # Months with 30 days
  elif month in thirty:
    validMaxDom = 30

  # Months with 31 days
  elif month in thirtyOne:
    validMaxDom = 31

  # Means our month was invalid
  else:
    validMaxDom = 0

  if day in range(1, validMaxDom + 1):
    return True
  else:
    return False


def validSep(data: str) -> bool:
  ''' Determine if matching valid separators were used '''
  if any((s in SEPARATORS) for s in data):
    separator = (set(SEPARATORS) & set(data)).pop()
    if data.count(separator) == 2:
      return True

  else:
    return True

  return False


# If the #{filename}.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
  main()
