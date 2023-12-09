'''
 Program: Date Converter GUI (Class for main wondow)
    Name: Andrew Dixon             File: dateCnvExceptions.py
    Date: 5 Feb 2019
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

#class Error(Exception):
#  "Base class for other exceptions"
#  pass

class FormatMaskNotFound(Exception):
  # "Format mas not found in valid format mask dictionaries"
  pass


class InputDateOrFormatMaskInvalid(Exception):
  # "Format mask/date is invalid"
  pass


class DateOutOfRange(Exception):
  # "Number passed is bigger than it should be for a valid date"
  pass


class OutputFormatInvalid(Exception):
  # "Format mask for output not found"
  pass