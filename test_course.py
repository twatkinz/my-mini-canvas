import pytest

@pytest.fixture
def arranged_user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager

@pytest.fixture
def arranged_course_manager():
    from course import CourseManager 
    my_course_manager = CourseManager()
    return my_course_manager

@pytest.fixture
def arranged_teacher_list(arranged_user_manager):
    arranged_user_manager.create_a_user("Miley Cyrus", "password", "teacher")
    teacher_ids = [1]
    teacher_list = arranged_user_manager.find_users(teacher_ids)
    return teacher_list

@pytest.fixture
def arranged_new_course(arranged_teacher_list):
    from course import Course
    new_course = Course(1, "COSC 381", "W24", arranged_teacher_list)
    return new_course


def test_generate_id(arranged_course_manager):
    # arrange
    new_count = arranged_course_manager.counter

    # act
    result = arranged_course_manager.generate_id()

    # assert
    assert(result == (new_count + 1))


def test_find_a_course_empty(arranged_course_manager):

    # act
    result = arranged_course_manager.find_a_course(3)

    # assert
    assert(result == None)


def test_find_a_course(arranged_course_manager, arranged_teacher_list):
    # arrange    
    new_course_id = arranged_course_manager.create_a_course("COSC 381", "W24", arranged_teacher_list)

    # act
    result = arranged_course_manager.find_a_course(new_course_id)

    #assert
    assert(result.course_id == new_course_id)
    assert(result.course_code == "COSC 381")
    assert(result.semester == "W24")
    for teacher in result.teacher_list:
        assert(teacher.type == "teacher")



def test_import_students(arranged_user_manager, arranged_new_course):
    # arrange
    arranged_user_manager.create_a_user("Harry Styles", "password", "student")
    arranged_user_manager.create_a_user("Beyonce", "password", "student")
    arranged_user_manager.create_a_user("Billie Eilish", "password", "student")
    student_ids = [2, 3, 4]
    student_list = arranged_user_manager.find_users(student_ids)

    # act 
    arranged_new_course.import_students(student_list)

    # assert
    for student in arranged_new_course.student_list:
        assert(student.type == "student")



def test_create_an_assignment(arranged_new_course):
    # arrange
    new_count = arranged_new_course.assignment_counter
    new_index = len(arranged_new_course.assignment_list)

    # act
    arranged_new_course.create_an_assignment("Dec 31")

    # assert
    assert(arranged_new_course.assignment_counter == (new_count + 1))
    assert(len(arranged_new_course.assignment_list) == (new_index + 1))
    assert(arranged_new_course.assignment_list[new_index].due_date == "Dec 31")


def test_generate_assignment_id(arranged_new_course):
    # arrange
    new_count = arranged_new_course.assignment_counter

    # act 
    result = arranged_new_course.generate_assignment_id()

    # assert
    assert(result == (new_count + 1))


def test_find_a_course_behavior(mocker, arranged_course_manager, arranged_teacher_list):
    # arrange    
    new_course_id = arranged_course_manager.create_a_course("COSC 381", "W24", arranged_teacher_list)
    mocked_find_a_course = mocker.patch('course.CourseManager.find_a_course')

    # act
    result = arranged_course_manager.find_a_course(new_course_id)

    #assert
    mocked_find_a_course.assert_called_with(new_course_id)


def test_import_students_behavior(mocker, arranged_user_manager, arranged_new_course):
    # arrange
    arranged_user_manager.create_a_user("Harry Styles", "password", "student")
    arranged_user_manager.create_a_user("Beyonce", "password", "student")
    arranged_user_manager.create_a_user("Billie Eilish", "password", "student")
    student_ids = [2, 3, 4]
    student_list = arranged_user_manager.find_users(student_ids)
    mocked_import_students = mocker.patch('course.Course.import_students')

    # act 
    arranged_new_course.import_students(student_list)

    # assert
    mocked_import_students.assert_called_with(student_list)


def test_create_an_assignment_behavior(mocker, arranged_new_course):
    # arrange
    new_count = arranged_new_course.assignment_counter
    new_index = len(arranged_new_course.assignment_list)
    mocked_create_an_assignment = mocker.patch('course.Course.create_an_assignment')

    # act
    arranged_new_course.create_an_assignment("Dec 31")

    # assert
    mocked_create_an_assignment.assert_called_with("Dec 31")


def test_create_a_course(mocker, arranged_course_manager, arranged_teacher_list):
    # arrange    
    new_index = len(arranged_course_manager.course_list)
    new_count = arranged_course_manager.counter
    mocked_create_a_course = mocker.patch('course.CourseManager.create_a_course')

    # act
    new_course_id = arranged_course_manager.create_a_course("COSC 381", "W24", arranged_teacher_list)

    # assert
    mocked_create_a_course.assert_called_with("COSC 381", "W24", arranged_teacher_list)