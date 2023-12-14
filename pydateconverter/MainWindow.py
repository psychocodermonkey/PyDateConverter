#! /usr/bin/env python3
'''
# Program: Python date information and conversion tool.
#    Name: Andrew Dixon            File: MainWindow.py
#    Date: 13 Dec 2023
#   Notes:
#
#........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3..
'''

from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtGui import QKeySequence, QShortcut
from pydateconverter import dateCnv as dc
from pydateconverter import dateCnvExceptions as ex

class MainWindow(QtWidgets.QMainWindow):
  """Class for main application window."""
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    uic.loadUi("pydateconverter/mainwindow.ui", self)
    self.loadFormats()
    self.convertButton.clicked.connect(self.convertButtonClicked)
    self.exitShortcut = QShortcut(QKeySequence('Esc'), self)
    self.exitShortcut.activated.connect(self.exitClicked)
    self.clipboard = QtWidgets.QApplication.clipboard()
    self.copyOutputShortcut = QShortcut(QKeySequence('Ctrl+C'), self)
    self.copyOutputShortcut.activated.connect(self.copyCLicked)

  def loadFormats(self) -> None:
    """Populate combo boxes with valid date formats."""
    formats = dc.validFormats()

    for fmt in formats:
      self.inputFormatComboBox.addItem(fmt)
      self.outputFormatComboBox.addItem(fmt)

  def convertButtonClicked(self) -> None:
    """Convert date from info provided on the form."""
    inDate = self.inputDateLineEdit.text()
    inFmt = self.inputFormatComboBox.currentText()
    otFmt = self.outputFormatComboBox.currentText()

    # Try and convert the date. If for whatever reason we get zero back, translate that to zero.
    try:
      cnvDate = dc.convertDate(inDate, inFmt, otFmt)
      if cnvDate == 0:
        cnvDate = ''

    # Handle exceptions passed up from the date converter and show the error in a dialog.
    except ex.FormatMaskNotFound:
      msg = 'Invalid format mask used.'
      self.sendUserErrorMessage(msg)
      return

    except ex.InputDateOrFormatMaskInvalid:
      msg = 'Issue with date object conversion, date or mask is invalid'
      self.sendUserErrorMessage(msg)
      return

    except ex.DateOutOfRange:
      msg = 'Date value is larger than it should be for a valid date'
      self.sendUserErrorMessage(msg)
      return

    except ex.OutputFormatInvalid:
      msg = 'Output date format is invalid'
      self.sendUserErrorMessage(msg)
      return

    # If all went well, update the output text box.
    self.outputDate.setText(str(cnvDate))

  # TODO: Figure out why ctrl+c isn't triggering this function.
  def copyCLicked(self) -> None:
    """Copy the text for the selected email template to the clipboard."""
    if len(self.outputDate.text()) > 0:
      self.clipboard.setText(self.outputDate.text())

  def sendUserErrorMessage(self, msg: str) -> None:
    """Send error emssage to the user."""
    userMessage = QtWidgets.QMessageBox()
    userMessage.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    userMessage.setWindowTitle("Error")
    userMessage.setText(msg)
    userMessage.exec()

  def exitClicked(self) -> None:
    """Close the form/application."""
    self.close()
