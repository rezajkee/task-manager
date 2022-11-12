import pytest
from django import urls
from task_manager.statuses.models import Status


@pytest.mark.django_db
@pytest.mark.parametrize("param", [("statuses"), ("create_status")])
def test_render_views(client, authenticated_user, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_status_creation(client, authenticated_user):
    assert Status.objects.count() == 0
    creation_url = urls.reverse("create_status")
    resp = client.post(creation_url, {"name": "first"})
    assert Status.objects.count() == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_status_creation_no_login(client):
    assert Status.objects.count() == 0
    creation_url = urls.reverse("create_status")
    resp = client.post(creation_url, {"name": "first"})
    assert Status.objects.count() == 0
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")


@pytest.mark.django_db
def test_status_update(client, test_status, authenticated_user):
    update_url = urls.reverse("update_status", kwargs={"pk": test_status.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("statuses")
    updated_status = Status.objects.get(id=test_status.id)
    assert updated_status.name == "not a test"


@pytest.mark.django_db
def test_status_update_no_login(client, test_status):
    update_url = urls.reverse("update_status", kwargs={"pk": test_status.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    updated_status = Status.objects.get(id=test_status.id)
    assert updated_status.name == test_status.name


@pytest.mark.django_db
def test_status_delete(client, test_status, authenticated_user):
    assert Status.objects.filter(id=test_status.id).exists() is True
    delete_url = urls.reverse("delete_status", kwargs={"pk": test_status.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("statuses")
    assert Status.objects.filter(id=test_status.id).exists() is False


@pytest.mark.django_db
def test_status_delete_no_login(client, test_status):
    delete_url = urls.reverse("delete_status", kwargs={"pk": test_status.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    assert Status.objects.filter(id=test_status.id).exists() is True


@pytest.mark.django_db
def test_status_in_task_delete(client, test_task, authenticated_user):
    delete_url = urls.reverse("delete_status", kwargs={"pk": test_task.status.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("statuses")
    assert Status.objects.filter(id=test_task.status.id).exists() is True