#! /usr/bin/env python3
'''
# Program: Python date information and conversion tool.
#    Name: Andrew Dixon            File: PyDateConverter.py
#    Date: 8 Dec 2023
#   Notes:
#
#........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3..
'''

import sys
import atexit
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton


class EmptyWindow(QWidget):

  def __init__(self):
    """ Constructor for Empty Window Class """
    super().__init__()
    self.initializeUI()

  def initializeUI(self):
    """Set up the application's GUI."""
    self.setGeometry(100, 100, 250, 150)
    self.setWindowTitle("Hello World!")

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    """Create and arrange widgets in the main window."""
    self.times_pressed = 0

    self.name_label = QLabel("Don't push the button.", self)
    self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.name_label.move(60, 30)

    self.button = QPushButton("Push Me", self)
    self.button.move(80, 70)
    self.button.clicked.connect(self.buttonClicked)

  def buttonClicked(self):
    """ Handle when the button is clicked. """
    self.times_pressed += 1

    match self.times_pressed:
      case 1:
        self.name_label.setText("Why'd you press me?")

      case 2:
        self.name_label.setText("I'm warning you.")
        self.button.setText("Feelin' Lucky?")
        self.button.adjustSize()
        self.button.move(70, 70)

      case 3:
        print("The window has been closed.")
        self.close()

      case _:
        print("You broke it!")
        self.times_pressed = 0

# Make sure we clean up anything we need to do if someone aborts the script
def onExit():
  try:
    # Try and do any clean up, error check as necessary
    pass
  except:
    # Deal with errors, or just ignore them by leaving this as "pass"
    pass
  return

# If the PyDateConverter.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
# Register the function to execute on ending the script
  atexit.register(onExit)
  app = QApplication(sys.argv)
  window = EmptyWindow()
  sys.exit(app.exec())
