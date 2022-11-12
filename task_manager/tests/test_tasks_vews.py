import pytest
from django import urls
from task_manager.tasks.models import Task


@pytest.mark.django_db
@pytest.mark.parametrize("param", [("tasks"), ("create_task")])
def test_render_views(client, authenticated_user, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_render_task(client, authenticated_user, test_task):
    temp_url = urls.reverse("detail_task", kwargs={"pk": test_task.id})
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_task_creation(client, authenticated_user, second_test_user, test_status):
    assert Task.objects.count() == 0
    creation_url = urls.reverse("create_task")
    resp = client.post(creation_url, {
        "name": "first",
        "author": authenticated_user.id,
        "status": test_status.id,
        "doer": second_test_user.id
    })
    assert Task.objects.count() == 1
    assert Task.objects.get(author=authenticated_user).doer == second_test_user
    assert resp.status_code == 302


@pytest.mark.django_db
def test_task_creation_no_login(client, second_test_user):
    assert Task.objects.count() == 0
    creation_url = urls.reverse("create_task")
    resp = client.post(creation_url, {
        "name": "first",
        "author": second_test_user.id
    })
    assert Task.objects.count() == 0
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")


@pytest.mark.django_db
def test_task_update(client, authenticated_user, test_task):
    update_url = urls.reverse("update_task", kwargs={"pk": test_task.id})
    resp = client.post(update_url, {
        "name": "not a test",
        "author": test_task.author.id,
        "status": test_task.status.id
    })
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tasks")
    updated_task = Task.objects.get(id=test_task.id)
    assert updated_task.name == "not a test"


@pytest.mark.django_db
def test_task_update_no_login(client, test_task):
    update_url = urls.reverse("update_task", kwargs={"pk": test_task.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    updated_task = Task.objects.get(id=test_task.id)
    assert updated_task.name == test_task.name


@pytest.mark.django_db
def test_task_delete_by_author(client, test_task_by_auth_user, authenticated_user):
    assert Task.objects.filter(id=test_task_by_auth_user.id).exists() is True
    delete_url = urls.reverse("delete_task", kwargs={"pk": test_task_by_auth_user.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tasks")
    assert Task.objects.filter(id=test_task_by_auth_user.id).exists() is False


@pytest.mark.django_db
def test_task_delete_no_login(client, test_task):
    delete_url = urls.reverse("delete_task", kwargs={"pk": test_task.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    assert Task.objects.filter(id=test_task.id).exists() is True


@pytest.mark.django_db
def test_task_delete_wrong_user(client, test_task, authenticated_user):
    delete_url = urls.reverse("delete_task", kwargs={"pk": test_task.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tasks")
    assert Task.objects.filter(id=test_task.id).exists() is True
