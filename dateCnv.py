#!/usr/local/bin/python3
#
# Program: Date converter functions
#    Name: Andrew Dixon             File: dateCnv
#    Date: 25 Oct 2018
#   Notes: For date converson to work date input must use valid separators.
#

from datetime import date, time, datetime, timedelta
from dateCnvExceptions import *

raiseExceptions = True

# Main -------------------------------------------------------------------------------------------------------
def main():
  """
  Run this as a standalone program
  """
  # Since we're going to handle reporting errors within here don't raise any exceptions
  global raiseExceptions
  raiseExceptions = False

  # Make this loop forever. Leave by putting a q/Q on the input line.
  while True:
    # Get the information from the user.
    inDate = input("Date to convert ((Q)uit): ")

    # Make it so that we can get out of our loop.
    if inDate.strip().upper().startswith("Q"):
      return

    inputFormat = input("Input format: ")
    outputFormat = input("Output format: ")

    # Print the converted date information. (convertDate(str, str, str, ?bool)).
    rtnVar = convertDate(inDate, inputFormat, outputFormat)

    # Print the output and if it was a numeric value or not.
    print("\nDate:> %s\n" % rtnVar)


# Output format mask for provided date format -----------------------------------------------------------------
def dateFormatMask(strFormat):
  """
  Return the format mask for the specified date format (no seperators)
  Be sure to update validFormats() when adding formats.
  """
  outFormat = {
    'MDY':'%m%d%y',
    'YMD':'%y%m%d',
    'DMY':'%d%m%y',
    'ISO':'%Y%m%d',
    'USA':'%m%d%Y',
    'EUR':'%d%m%Y',
    'JIS':'%Y%m%d',
    'JUL':'%y%j',
    'LJUL':'%Y%j',
    'HUN':'HUN'
  }

  try:
    fmtString = outFormat[strFormat.upper()]

  except KeyError:
    if raiseExceptions:
      raise FormatMaskNotFound
      #raise Exception(">> ERROR: Format mask for %s not found." % strFormat)
      return None
    else:
      print(">> ERROR: Format mask for %s not found." % strFormat)

      # Return the passed value as it's the best we have, also makes later error reporting make sense
      return strFormat

  return fmtString


# Output format mask for provided date format with separators -------------------------------------------------
def dateFormatSeparatedMask(strFormat, separator):
  """
  Return the format mask for the specified date format (with seperators)
  Be sure to update validFormats() when adding formats.
  """
  outFormat = {
    'MDY':'%m?%d?%y',
    'YMD':'%y?%m?%d',
    'DMY':'%d?%m?%y',
    'ISO':'%Y?%m?%d',
    'USA':'%m?%d?%Y',
    'EUR':'%d?%m?%Y',
    'JIS':'%Y?%m?%d',
    'JUL':'%y?%j',
    'LJUL':'%Y?%j',
    'HUN':'HUN'
  }

  try:
    fmtString = outFormat[strFormat.upper()]
    fmtString = fmtString.replace("?", separator)

  except KeyError:
    if raiseExceptions:
      raise FormatMaskNotFound
      return None
    else:
      print(">> ERROR: Format mask for %s not found." % strFormat)
      # Return the passed value as it's the best we have, also makes later error reporting make sense
      return strFormat

  return fmtString


# Return list of valid formats --------------------------------------------------------------------------------
def validFormats():
  """
  Return the valid formats that are handled with in here.
  Be sure to update this dictionary if adding additional format masks.
  """
  dteFormats = ('MDY', 'YMD', 'DMY', 'ISO', 'USA', 'EUR', 'JIS', 'JUL', 'LJUL', 'HUN')
  return dteFormats


# Convert the date from format to another ---------------------------------------------------------------------
def convertDate(inDate, inFmt, otFmt, otMatch=True):
  """
  Use the passed information to convert the date.
  """
  # Valid separators used in dates.
  SEPARATORS = set(".,-/ ")

  # Look for any valid separators provided in the date.
  if any((s in SEPARATORS) for s in inDate):
    separatorsProvided = True

    # Get the separator that was used in the string. If there were multiples this will cause a problem.
    separator = (set(SEPARATORS) & set(inDate)).pop()
  else:
    separatorsProvided = False

  # If ther was a seperator provided in the string fetch the mmask with the separator, otherwise without.
  if separatorsProvided and otMatch:
    inFmt = dateFormatSeparatedMask(inFmt, separator)
    otFmt = dateFormatSeparatedMask(otFmt, separator)

  # If we don't want separators to match handle converting the input.
  elif separatorsProvided and not otMatch:
    inFmt = dateFormatSeparatedMask(inFmt, separator)
    otFmt = dateFormatMask(otFmt)

  # If we don't want separators to match handle converting the output, default to /.
  #  Commenting this out to to use this to convert dates to actual numbers, seems more useful.
  #elif not separatorsProvided and not otMatch:
  #  inFmt = dateFormatMask(inFmt)
  #  otFmt = dateFormatSeparatedMask(otFmt, "/")

  # Handle using no separators
  else:
    inFmt = dateFormatMask(inFmt)
    otFmt = dateFormatMask(otFmt)

  # Hundred year has to be handled differently than other formats.
  if inFmt != 'HUN':
    try:
      dtDate = datetime.strptime(inDate, inFmt)

    # If something went wrong, it is either the information or the format asked for.
    except ValueError:
      if raiseExceptions:
        raise InputDateOrFormatMaskInvalid
        return None
      else:
        print(">> ERROR: Input date or format mask is invalid. Date: %s - Format/Mask: %s" % (inDate, inFmt))
        return 0

  else: # inFmt == 'HUN'
    dtDate = datetime.strptime('19000101', '%Y%m%d')
    dtDelta = timedelta(days=int(inDate))
    try:
      dtDate += dtDelta

    except OverflowError:
      if raiseExceptions:
        raise DateOutOfRange
        return None
      else:
        print(">> ERROR: Date is out of range: %s" % (inDate))
        # no reason not to just return max date instead of zero
        dtDate = datetime.strptime('99991231', '%Y%m%d')

  if otFmt != 'HUN':
    try:
      rtDate = dtDate.strftime(otFmt)

    # If there was an issue, then there was a problem with the format.
    except ValueError:
      if raiseExceptions:
        raise OutputFormatInvalid
        return None
      else:
        print(">> ERROR: Output format is invalid. - Format/Mask: %s" % (otFmt))
        return 0

  else: # otFmt == 'HUN'
    hunDate = datetime.strptime('19000101', '%Y%m%d')
    rtDate = abs((hunDate - dtDate).days)

  # If a string has to be returned, return a string otherwise make sure it's a numeric return
  if separatorsProvided and otMatch:
    return rtDate
  else:
    return int(rtDate)


# If the dateCnv.py is run (instead of imported as a module), call the main() function:
if __name__ == '__main__': main()
