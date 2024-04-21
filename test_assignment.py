import pytest

@pytest.fixture
def arranged_assignment():
    from assignment import Assignment
    my_assignment = Assignment(1, 1, 1)
    return my_assignment

@pytest.fixture
def arranged_submission():
    from assignment import Submission
    my_submission = Submission(1, "homework")
    return my_submission


def test_submit(arranged_assignment, arranged_submission):  
    # arrange
    new_index = len(arranged_assignment.submission_list)
    
    # act
    arranged_assignment.submit(arranged_submission)
    
    # assert
    assert(len(arranged_assignment.submission_list) == (new_index + 1))
    assert(arranged_assignment.submission_list[0].submission == "homework")
    assert(arranged_assignment.submission_list[0].student_id == 1)


def test_submit_behavior(mocker, arranged_assignment, arranged_submission):
    # arrange
    new_index = len(arranged_assignment.submission_list)
    mocked_submit = mocker.patch('assignment.Assignment.submit')

    # act
    arranged_assignment.submit(arranged_submission)
    
    # assert
    mocked_submit.assert_called_with(arranged_submission)