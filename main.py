import os
import csv

csv_path = "Bush School Student (Responses).csv"

def writeToTrainFile():
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            print(row)


if __name__ == '__main__':
    writeToTrainFile()
