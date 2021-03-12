

def course_file_location(instance, filename):
    return "{}/{}/{}/{}".format(
        instance.section.course.id,
        instance.section.id,
        instance.id,
        filename,
    )


def assignment_file_location(instance, filename):
    return "{}/{}/{}/{}".format(
        instance.assignment.course.id,
        instance.assignment.id,
        instance.id,
        filename,
    )

def assignment_solution_file_location(instance, filename):
    return "{}/{}/{}/{}".format(
        instance.assignment_solution.assignment.course.id,
        instance.assignment_solution.assignment.id,
        instance.id,
        filename,
    )