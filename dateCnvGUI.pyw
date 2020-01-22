#!/usr/local/bin/python3
#
# Program: Date converter GUI front end
#    Name: Andrew Dixon             File: dateCnvGUI
#    Date: 30 Oct 2018
#   Notes: On windows use .pyw extension to hide the terminal window
#

from tkinter import *
from tkinter import ttk
from dateCnv import convertDate, validFormats
from dateCnvExceptions import *


def submit():
  # Reset the output field
  output.configure(state='normal')
  output.delete(0.0, END)
  output.configure(state='disabled')

  errOutput.delete(0.0, END)

  # Get the information from the fields
  txtInDate = inDate.get()
  txtInFmt = inFmt.get()
  txtOtFmt = otFmt.get()

  # Try the date conversion with the data provided.
  try:
    cnvDate = convertDate(txtInDate, txtInFmt, txtOtFmt)
    if cnvDate == 0: cnvDate = ''

  # Handle exceptions passed up from the date converter
  except FormatMaskNotFound:
    errOutput.insert(END, 'Invalid Format mask used')
    return

  except InputDateOrFormatMaskInvalid:
    errOutput.insert(END, 'Issue with date object conversion, date or mask is invalid')
    return

  except DateOutOfRange:
    errOutput.insert(END, 'Date value is larger than it should be for a valid date')
    return

  except OutputFormatInvalid:
    errOutput.insert(END, 'Output date format is invalid')
    return

  except Exception as e:
    errOutput.insert(END, e)
    return

  # Set the output field and keep it protected from inadvertant changes
  output.configure(state='normal')
  output.insert(END, cnvDate)
  output.configure(state='disabled')


# Setup the main window -----------------------------------------------------------------------------------------------
root = Tk()
root.title('Date Converter')
root.configure(background='black')

# Setup a frame so we can have an easy border
root_frame = Frame(root, bd=10, bg='black')
root_frame.pack()

# Setup the Labels for the fields
Label(root_frame, text='Enter date: ', bg='black', fg='white', font='none 12 bold').grid(row=0, column=0, sticky=E)
Label(root_frame, text='Entry format: ', bg='black', fg='white', font='none 12 bold').grid(row=1, column=0, sticky=E)
Label(root_frame, text='Output format: ', bg='black', fg='white', font='none 12 bold').grid(row=2, column=0, sticky=E)

# Setup the text boxes to for the input
inDate = Entry(root_frame, width=12, bg='white')
inDate.grid(row=0, column=1, sticky=E)

# Setup the list for the date formats
dteFormats = validFormats()

# Setup the combo boxes for the formats using the list of valid formats.
inFmt = StringVar()
inFmtDD = ttk.Combobox(root_frame, width=9, textvariable=inFmt)
inFmtDD['values'] = dteFormats
inFmtDD.grid(row=1, column=1, sticky=E)

otFmt = StringVar()
otFmtDD = ttk.Combobox(root_frame, width=9, textvariable=otFmt)
otFmtDD['values'] = dteFormats
otFmtDD.grid(row=2, column=1, sticky=E)

# Setup the submit button
Button(root_frame, text='Convert', width=7, command=submit).grid(row=3, column=1, sticky=E)

# Setup the output section
Label(root_frame, text='\nConverted Date: ', bg='black', fg='white', font='none 12 bold').grid(row=4, column=0, sticky=W)

output = Text(root_frame, width=12, height=1, bg='black', fg='white', state='disabled')
output.grid(row=4, column=1, sticky=E)

# Setup the error box at the bottom of the window.
errOutput = Text(root_frame, width=28, height=3, wrap=WORD, bg='black', fg='white', relief='flat')
errOutput.grid(row=5, column=0, columnspan=2, sticky=S)

# Run the main loop for the window
root.mainloop()
