import os
import csv
from tkinter import filedialog, messagebox
from tkinter import *


def ReadCsv():
    # gui to select file
    csv_path = filedialog.askopenfilename(
        initialdir="/", title="Select CSV File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    # print
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)


if __name__ == '__main__':
    ReadCsv()
