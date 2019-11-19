
PROJECT_MIN = 6
PROJECT_MAX = 10

# Create dictionary where key is the project name and value is project object
# Purpose: easy access to project object for modification
def populate_project_dict(projects: list):
    project_dict = {}
    for project in projects:
        project_dict[project.title] = project
    return project_dict

def assign_first_choices(students: list, projects: dict):
    for student in students:
        first_choice_name = student.preferences['1']
        projects[first_choice_name].students.append(student)

def valid_project_student_sizes(projects: dict):
    for project in projects.values():
        if len(project.students) < PROJECT_MIN and len(project.students) > PROJECT_MAX:
            return False
    return True

# Starting Point
def run_matching(students: list, projects: list):
    projects_dict = populate_project_dict(projects)

    # Step 2
    assign_first_choices(students, projects_dict)

    # Step 3
    if valid_project_student_sizes(projects_dict):
        return list(projects_dict.values())

    # Step 
