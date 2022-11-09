import pytest
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status


@pytest.fixture
def user_reg_data():
    return {
        "first_name": "Tom",
        "last_name": "Hanks",
        "username": "Thanks",
        "password1": "qwerty",
        "password2": "qwerty",
    }


@pytest.fixture
def user_creation_data():
    return {
        "first_name": "Keanu",
        "last_name": "Reeves",
        "username": "Silverhand",
        "password": "2077",
    }


@pytest.fixture
def user_update_data():
    return {
        "username": "Neo",
        "password1": "MatrixHasU",
        "password2": "MatrixHasU",
    }


@pytest.fixture
def create_test_user(user_creation_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_creation_data)
    return test_user


@pytest.fixture
def authenticated_user(client, user_creation_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_creation_data)
    test_user.save()
    client.login(**user_creation_data)
    return test_user


@pytest.fixture
def second_test_user(user_reg_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(
        username=user_reg_data.get("username"),
        password=user_reg_data.get("password"),
    )
    test_user.save()
    return test_user


@pytest.fixture
def test_status():
    test_status = Status.objects.create(name="test")
    test_status.save()
    return test_status
