import os
import csv

csv_path = "path_to_csv"


def writeToTrainFile():
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            print(row)
