# from main import Student, Project
import heapq
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
        if len(project.students) < PROJECT_MIN and len(project.students) > PROJECT_MAX:
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
    projects_dict = populate_project_dict(projects)

    # Step 2
    assign_first_choices(students, projects_dict)

    # Step 3
    if valid_project_student_sizes(projects_dict):
        # print("valid 1st")
        return list(projects_dict.values())

    # Step 4
    for student in students:
        student.compatibility = assign_compatibility(student, projects)
        # print(student.compatibility)

    # Step 5
    ProjectList = []
    for project in projects:
        StudentList = []
        for student in students:
            data = (student.compatibility[project.title], student.name)
            StudentList.append(data)
        ProjectList.append(StudentList)

    for i in range(len(ProjectList)):
        ProjectList[i] = sorted(ProjectList[i], reverse=True)
        # print(ProjectList[i])
    ProjectList = sorted(ProjectList, reverse=True)

    for i in range(PROJECT_MAX):
        for StudentList in ProjectList:
            if(i < len(StudentList)):
                name = StudentList[i][1]
                # print(f"removing {name}")
                for StudentList2 in ProjectList:
                    for data in StudentList2:
                        if data[1] == name and StudentList != StudentList2:
                            StudentList2.remove(data)
                            # print(StudentList2)

    for i in range(len(ProjectList)):
        print(projects[i].title, ProjectList[i])
