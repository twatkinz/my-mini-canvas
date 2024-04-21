import pytest

@pytest.fixture
def arranged_user_manager():
    from user import UserManager
    my_user_manager = UserManager()
    return my_user_manager

@pytest.fixture
def arranged_user_ids(arranged_user_manager):
    arranged_user_manager.create_a_user("Miley Cyrus", "password", "teacher")
    arranged_user_manager.create_a_user("Harry Styles", "password", "student")
    arranged_user_manager.create_a_user("Beyonce", "password", "student")
    arranged_user_manager.create_a_user("Billie Eilish", "password", "student")
    ids = (1, 2, 3)
    return ids


def test_generate_id(arranged_user_manager):
    # arrange
    new_count = arranged_user_manager.counter

    # act
    result = arranged_user_manager.generate_id()

    # assert
    assert(result == (new_count + 1))


def test_create_a_user(arranged_user_manager):
    # arrange
    new_index = len(arranged_user_manager.user_list)
    new_count = arranged_user_manager.counter

    # act 
    arranged_user_manager.create_a_user("Miley Cyrus", "password", "teacher")

    # assert
    assert((len(arranged_user_manager.user_list)) == (new_index + 1))
    assert(arranged_user_manager.user_list[new_index].name == "Miley Cyrus")
    assert(arranged_user_manager.user_list[new_index].password == "password")
    assert(arranged_user_manager.user_list[new_index].type == "teacher")
    assert(arranged_user_manager.counter == (new_count + 1))


def test_find_users_empty(arranged_user_manager):

    # act
    ids = (1, 2, 3)
    result = arranged_user_manager.find_users(ids)

    # assert
    assert(result == "Users not found")


def test_find_users(arranged_user_manager, arranged_user_ids):

    # act
    result = arranged_user_manager.find_users(arranged_user_ids)

    # assert
    assert(result[0].name == "Miley Cyrus")
    assert(result[1].name == "Harry Styles")
    assert(result[2].name == "Beyonce")
    assert(result[0].type == "teacher")
    assert(result[1].type == "student")


def test_find_users_behavior(mocker, arranged_user_manager, arranged_user_ids):
    # arrange
    mocked_find_users = mocker.patch('user.UserManager.find_users')
   
    # act
    result = arranged_user_manager.find_users(arranged_user_ids)

    # assert
    mocked_find_users.assert_called_with(arranged_user_ids)



def test_create_a_user_behavior(mocker, arranged_user_manager):
    # arrange
    new_index = len(arranged_user_manager.user_list)
    new_count = arranged_user_manager.counter
    mocked_create_a_user = mocker.patch('user.UserManager.create_a_user')

    # act 
    arranged_user_manager.create_a_user("Miley Cyrus", "password", "teacher")

    # assert
    mocked_create_a_user.assert_called_with("Miley Cyrus", "password", "teacher")