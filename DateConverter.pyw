#!/usr/local/bin/python3
'''
 Program:
    Name: Andrew Dixon            File: DateConverter.pyw
    Date: Feb 5 2019
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

from tkinter import Frame, Tk, Label, Button, Text, StringVar, messagebox,\
   E, W, SE, Entry, END, ttk
from pydateconverter import dateCnv as cnv
from pydateconverter import dateCnvExceptions as ex


def main():
  """ Main """
  root = Tk()
  root.title('Date Converter')
  MainWindow(root)
  root.mainloop()


class MainWindow:
  """ Primary window class """
  def __init__(self, master):
    # Setup a frame so we can have an easy border
    root_frame = Frame(master, bd=10, bg='black')
    root_frame.pack()

    # Setup the Labels for the input fields
    Label(root_frame, text='Enter date: ', bg='black', fg='white', font='none 12 bold')\
      .grid(row=0, column=0, sticky=E)
    Label(root_frame, text='Entry format: ', bg='black', fg='white', font='none 12 bold')\
      .grid(row=1, column=0, sticky=E)
    Label(root_frame, text='Output format: ', bg='black', fg='white', font='none 12 bold')\
      .grid(row=2, column=0, sticky=E)

    # Setup the text boxes to for the input
    # self.inDate = Entry(root_frame, width=12, bg='white', fg='black')
    self.inDate = Entry(root_frame, width=12)
    self.inDate.grid(row=0, column=1, sticky=E)

    # Get the list of valid formats from the date converter
    self.dteFormats = cnv.validFormats()

    # Setup the combo boxes for the formats using the list of valid formats.
    self.inFmt = StringVar()
    self.inFmtDD = ttk.Combobox(root_frame, width=9, textvariable=self.inFmt)
    self.inFmtDD['values'] = self.dteFormats
    self.inFmtDD.grid(row=1, column=1, sticky=E)

    self.otFmt = StringVar()
    self.otFmtDD = ttk.Combobox(root_frame, width=9, textvariable=self.otFmt)
    self.otFmtDD['values'] = self.dteFormats
    self.otFmtDD.grid(row=2, column=1, sticky=E)

    # Setup the submit button
    Button(root_frame, text='Convert', width=7, command=self.submit)\
      .grid(row=3, column=1, sticky=E)

    # Setup the output section (Label and output text box)
    Label(root_frame, text='\nConverted Date: ', bg='black', fg='white', font='none 12 bold')\
      .grid(row=4, column=0, sticky=W)

    self.output = Text(root_frame, width=12, height=1, bg='black', fg='white', state='disabled')
    self.output.grid(row=4, column=1, sticky=SE)


  def submit(self):
    """ Submit Button """
    # Reset the output field
    self.output.configure(state='normal')
    self.output.delete(0.0, END)
    self.output.configure(state='disabled')

    # Get the information from the fields
    txtInDate = self.inDate.get()
    txtInFmt = self.inFmt.get()
    txtOtFmt = self.otFmt.get()

    # Try the date conversion with the data provided.
    try:
      cnvDate = cnv.convertDate(txtInDate, txtInFmt, txtOtFmt)
      if cnvDate == 0:
        cnvDate = ''

    # Handle exceptions passed up from the date converter
    except ex.FormatMaskNotFound:
      messagebox.showerror(title='<< ERROR >>',\
         message='Invalid format mask used.')
      return

    except ex.InputDateOrFormatMaskInvalid:
      messagebox.showerror(title='<< ERROR >>',\
         message='Issue with date object conversion, date or mask is invalid')
      return

    except ex.DateOutOfRange:
      messagebox.showerror(title='<< ERROR >>',\
        message='Date value is larger than it should be for a valid date')
      return

    except ex.OutputFormatInvalid:
      messagebox.showerror(title='<< ERROR >>',\
        message='Output date format is invalid')
      return

    except Exception as e:
      messagebox.showerror(title='<< ERROR >>', message=e)
      return

    # Set the output field and keep it protected from inadvertant changes
    self.output.configure(state='normal')
    self.output.insert(END, cnvDate)
    self.output.configure(state='disabled')


# If the DateConverter.py is run (instead of imported as a module), call the main() function:
if __name__ == '__main__':
  main()
