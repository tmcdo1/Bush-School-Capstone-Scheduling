# from main import Student, Project
from tkinter import messagebox
PROJECT_MIN = 6
PROJECT_MAX = 10

# Create dictionary where key is the project name and value is project object
# Purpose: easy access to project object for modification


def populate_project_dict(projects: list):
    project_dict = {}
    for project in projects:
        project_dict.update({project.title: project})
    return project_dict


def assign_first_choices(students: list, projects: dict):
    for student in students:
        first_choice_name = student.preferences[1]
        projects[first_choice_name].students.append(student)


def valid_project_student_sizes(projects: dict):
    for project in projects.values():
        if len(project.students) < PROJECT_MIN or len(project.students) > PROJECT_MAX:
            return False
    return True


def assign_compatibility(student, projects: list):
    compatibility_dict = {}
    for project in projects:
        compatibility = 0.0

        # preference
        if project.title == student.preferences[1]:
            compatibility += 1.0 * 60.0
        elif project.title == student.preferences[2]:
            compatibility += 0.66 * 60.0
        elif project.title == student.preferences[3]:
            compatibility += 0.33 * 60.0

        # skills
        numSkills = 0
        for skill in student.skills:
            if skill in project.skills:
                numSkills += 1
        if numSkills == 3:
            compatibility += 1.0 * 25.0
        elif numSkills == 2:
            compatibility += 0.66 * 25.0
        elif numSkills == 1:
            compatibility += 0.33 * 25.0

        # track
        if student.track == project.track:
            compatibility += 10.0

        # research
        # ignored for now
        compatibility += 5

        # experience
        # ignored for now
        compatibility_dict.update({project.title: compatibility})
    return compatibility_dict


# Starting Point

def run_matching(students: list, projects: list):

    # Step 1
    projects_dict = populate_project_dict(projects)

    # Step 2
    assign_first_choices(students, projects_dict)

    # Step 3
    if valid_project_student_sizes(projects_dict):
        # print("valid 1st")
        messagebox.showinfo(
            "Matched!", "All students placed in their first choice projects.")
        return list(projects_dict.values())

    # Step 4
    for student in students:
        student.compatibility = assign_compatibility(student, projects)

    list1 = run_matching_school_based(students, projects)
    list2 = run_matching_student_based(students, projects)

    data_str = ""
    for (projTitle, studentList) in list1:
        new_title = projTitle.replace(",", "[comma]")
        data_str += new_title
        for student in studentList:
            data_str = data_str + ", " + student[1]
        data_str += "\n"
    f = open("project_based.csv", "w")
    f.write(data_str)
    f.close()

    data_str = ""
    for (projTitle, studentList) in list2:
        data_str += projTitle
        for student in studentList:
            data_str = data_str + ", " + student[1]
        data_str += "\n"
    f = open("student_based.csv", "w")
    f.write(data_str)
    f.close()

    # list3 = run_matching3(students, projects)


def run_matching_school_based(students: list, projects: list):

    # populating projects
    projects_dict = populate_project_dict(projects)

    # populating all projects with all students
    for project in projects:
        studentList = []
        # generating student list for each project based on compatibility
        for student in students:
            data = (student.compatibility[project.title], student.name)
            studentList.append(data)
        projects_dict.update({project.title: studentList})

    # sorting student lists in projects
    for projectTitle in projects_dict.keys():
        projects_dict.update(
            {projectTitle: sorted(projects_dict[projectTitle], reverse=True)})

    # sorting projects based on the hghest student compatibility score
    projects_list = sorted(projects_dict.items(),
                           key=lambda kv: kv[1], reverse=True)

    # replacing students as best fit by the project after
    # min number of students in project met
    # ALGORITHM: Fix 1st student in 1st project. remove him/her from the rest.
    # Then the 1st in the 2nd project and continue until 1st students in all projects are fixed.
    # Then the 2nd in the 1st project and so on...
    for i in range(PROJECT_MAX):
        for (projTitle, studentList) in projects_list:
            if(i < len(studentList)):
                name = studentList[i][1]
                for (projTitle2, studentList2) in projects_list:
                    for data in studentList2:
                        if data[1] == name and studentList != studentList2:
                            studentList2.remove(data)

    return projects_list


def run_matching_student_based(students: list, projects: list):

    # populating projects
    projects_dict = populate_project_dict(projects)

    # populating all projects with the first choice students
    for project in projects:
        studentList = []
        # generating student list for each project based on first choice and compatibility
        for student in students:
            first_choice_name = student.preferences[1]
            if project.title == first_choice_name:
                data = (
                    student.compatibility[project.title], student.name, student.preferences)
                studentList.append(data)
        projects_dict.update({project.title: studentList})

    # sorting student lists in projects
    for projectTitle in projects_dict.keys():
        projects_dict.update(
            {projectTitle: sorted(projects_dict[projectTitle], reverse=True)})

    # sorting projects based on the student sizes
    projects_list = sorted(projects_dict.items(),
                           key=lambda k: len(k[1]), reverse=True)

    minimum_met = {}
    maximum_exceeded = {}
    for (projTitle, studentList) in projects_list:
        # che(cking if minimum number of students are filled
        if len(studentList) < PROJECT_MIN:
            minimum_met.update({projTitle: False})
        else:
            minimum_met.update({projTitle: True})

        # checking if maximum number of students are exceeded
        if len(studentList) > PROJECT_MAX-1:
            maximum_exceeded.update({projTitle: True})
        else:
            maximum_exceeded.update({projTitle: False})

    projects_dict = {}
    for (projTitle, studentList) in projects_list:
        projects_dict.update({projTitle: studentList})

    # sorting first go: projects exceeding max students to send exceeding ones into second choices
    for (projTitle, studentList) in projects_list:
        if maximum_exceeded[projTitle]:
            for i in range(len(studentList) - 1, PROJECT_MAX - 1, -1):
                second_project = studentList[i][2][2]
                if (not minimum_met[second_project]):
                    projects_dict[second_project].append(
                        studentList[i])
                    projects_dict[projTitle].remove(studentList[i])
                    if len(projects_dict[second_project]) >= PROJECT_MIN:
                        minimum_met.update(
                            {second_project: True})
            for i in range(len(studentList) - 1, PROJECT_MAX - 1, -1):
                second_project = studentList[i][2][2]
                if (not maximum_exceeded[second_project]):
                    projects_dict[second_project].append(
                        studentList[i])
                    projects_dict[projTitle].remove(studentList[i])
                    if len(projects_dict[second_project]) > PROJECT_MAX-1:
                        maximum_exceeded.update(
                            {second_project: True})

    # sorting projects based on the student sizes
    projects_list = sorted(projects_dict.items(),
                           key=lambda k: len(k[1]), reverse=True)

    for (projTitle, studentList) in projects_list:
        # che(cking if minimum number of students are filled
        if len(studentList) < PROJECT_MIN:
            minimum_met.update({projTitle: False})
        else:
            minimum_met.update({projTitle: True})

        # checking if maximum number of students are exceeded
        if len(studentList) > PROJECT_MAX-1:
            maximum_exceeded.update({projTitle: True})
        else:
            maximum_exceeded.update({projTitle: False})

    # sorting second go: projects exceeding max students to send exceeding ones into third choices
    for (projTitle, studentList) in projects_list:
        if maximum_exceeded[projTitle]:
            for i in range(len(studentList) - 1, PROJECT_MAX - 1, -1):
                third_project = studentList[i][2][3]
                if (not minimum_met[third_project]):
                    projects_dict[third_project].append(
                        studentList[i])
                    projects_dict[projTitle].remove(studentList[i])
                    if len(projects_dict[third_project]) >= PROJECT_MIN:
                        minimum_met.update(
                            {third_project: True})
            for i in range(len(studentList) - 1, PROJECT_MAX - 1, -1):
                third_project = studentList[i][2][3]
                if (not maximum_exceeded[third_project]):
                    projects_dict[third_project].append(
                        studentList[i])
                    projects_dict[projTitle].remove(studentList[i])
                    if len(projects_dict[third_project]) > PROJECT_MAX-1:
                        maximum_exceeded.update(
                            {third_project: True})

    projects_list = sorted(projects_dict.items(),
                           key=lambda k: len(k[1]), reverse=True)

    return projects_list
