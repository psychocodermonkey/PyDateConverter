#class Error(Exception):
#  "Base class for other exceptions"
#  pass

class FormatMaskNotFound(Exception):
  ''' Format mas not found in valid format mask dictionaries '''
  # pass


class InputDateOrFormatMaskInvalid(Exception):
  ''' Format mask/date is invalid '''
  # pass


class DateOutOfRange(Exception):
  ''' Number passed is bigger than it should be for a valid date '''
  # pass


class OutputFormatInvalid(Exception):
  ''' Format mask for output not found '''
  # pass
