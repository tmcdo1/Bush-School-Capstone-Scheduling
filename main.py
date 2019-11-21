import os
import csv
from tkinter import filedialog, messagebox
from tkinter import *
from algo import run_matching


class Project:
    title: str

    track: str

    # skills = list of str
    skills: list

    # list of Student objects
    students: list


class Student:
    name: str

    uin: int

    # preferences = {rank : project_title}
    preferences: dict

    # compatibility = {project_title : score}
    compatibility: dict

    track = str

    # skills = list of str
    skills: list

    # research_interest = list of str
    research_interest: list

    relevant: bool

    addition_details: str


# list of all projects
projects = []

# list of students
students = []


def readProjectCsv():
    # csv_path = filedialog.askopenfilename(
    #     initialdir="/", title="Select Project CSV File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    csv_path = "/Users/shreyshah/Projects/Bush-School-Capstone-Scheduling/Bush Faculty (Responses).csv"
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            proj = Project()

            proj.title = row[1]

            proj.track = row[2]

            proj.skills = row[3].split(', ')
            for skill in row[4].split(', '):
                proj.skills.append(skill)
            proj.skills.remove('')

            proj.students = []
            projects.append(proj)


def readStudentCsv():
    # gui to select file
    # csv_path = filedialog.askopenfilename(
    #     initialdir="/", title="Select Student CSV File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    csv_path = "/Users/shreyshah/Projects/Bush-School-Capstone-Scheduling/Bush School Student (Responses).csv"

    # print
    with open(csv_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            person = Student()

            person.name = row[1]

            person.uin = row[2]

            person.preferences = {1: row[3], 2: row[4], 3: row[5]}

            person.track = row[6]

            person.skills = row[7].split(', ')

            person.research_interest = row[8].split(', ')

            person.relevant = (row[9] == 'Yes')

            if (person.relevant):
                person.addition_details = row[10]

            person.compatibility = {}
            for proj in projects:
                person.compatibility.update({proj.title: 0.0})

            students.append(person)


if __name__ == '__main__':
    readProjectCsv()
    # for proj in projects:
    #     print(proj.skills)
    readStudentCsv()
    # for stud in students:
    #     print(stud.compatibility)
    #     print(stud.preferences)
    run_matching(students, projects)
