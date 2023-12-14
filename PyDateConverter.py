#! /usr/bin/env python3
'''
# Program: Python date converter main application.
#    Name: Andrew Dixon            File: PyDateConverter.py
#    Date: 13 Dec 2023
#   Notes:
#
#........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3..
'''

import sys
from PyQt6.QtWidgets import QApplication
from pydateconverter.MainWindow import MainWindow


# If the PyDateConverter.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
