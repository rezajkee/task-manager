import pytest
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tags.models import Tag
from task_manager.tasks.models import Task


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
        "first_name": "Keanu",
        "last_name": "Reeves",
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
        first_name=user_reg_data.get("first_name"),
        last_name=user_reg_data.get("last_name"),
        username=user_reg_data.get("username"),
        password=user_reg_data.get("password1"),
    )
    test_user.save()
    return test_user


@pytest.fixture
def test_status():
    test_status = Status.objects.create(name="test")
    test_status.save()
    return test_status


@pytest.fixture
def test_tag():
    test_tag = Tag.objects.create(name="test")
    test_tag.save()
    return test_tag


@pytest.fixture
def test_task(second_test_user, test_status, test_tag):
    test_task = Task.objects.create(
        name="test", author=second_test_user, status=test_status, tags=test_tag
    )
    test_task.save()
    return test_task


@pytest.fixture
def test_task_by_auth_user(authenticated_user, test_status):
    test_task = Task.objects.create(
        name="test", author=authenticated_user, status=test_status
    )
    test_task.save()
    return test_task