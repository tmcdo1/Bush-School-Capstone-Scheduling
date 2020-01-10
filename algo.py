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
        return list(projects_dict.values())

    # Step 4
    for student in students:
        student.compatibility = assign_compatibility(student, projects)

    list1 = run_matching_school_based(students, projects)
    print(list1)
    f = open("demo.txt", "w")
    f.write(list1)
    f.close()

    # list3 = run_matching3(students, projects)


def run_matching_school_based(students: list, projects: list):

    projects_dict = populate_project_dict(projects)

    # populating all projects with all students
    for project in projects:
        sutdentList = []
        # generating student list for each project based on compatibility
        for student in students:
            data = (student.compatibility[project.title], student.name)
            sutdentList.append(data)
        projects_dict.update({project.title: sutdentList})

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
        for (projTitle, sutdentList) in projects_list:
            if(i < len(sutdentList)):
                name = sutdentList[i][1]
                for (projTitle2, sutdentList2) in projects_list:
                    for data in sutdentList2:
                        if data[1] == name and sutdentList != sutdentList2:
                            sutdentList2.remove(data)

    return projects_list


def run_matching_student_based(students: list, projects: list):

    # Step 1
    projects_dict = populate_project_dict(projects)

    
    return []
