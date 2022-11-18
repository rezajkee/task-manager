import pytest
from django import urls
from task_manager.labels.models import Label


@pytest.mark.django_db
@pytest.mark.parametrize("param", [("labels"), ("create_label")])
def test_render_views(client, authenticated_user, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_label_creation(client, authenticated_user):
    assert Label.objects.count() == 0
    creation_url = urls.reverse("create_label")
    resp = client.post(creation_url, {"name": "first"})
    assert Label.objects.count() == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_label_creation_no_login(client):
    assert Label.objects.count() == 0
    creation_url = urls.reverse("create_label")
    resp = client.post(creation_url, {"name": "first"})
    assert Label.objects.count() == 0
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")


@pytest.mark.django_db
def test_label_update(client, test_label, authenticated_user):
    update_url = urls.reverse("update_label", kwargs={"pk": test_label.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("labels")
    updated_label = Label.objects.get(id=test_label.id)
    assert updated_label.name == "not a test"


@pytest.mark.django_db
def test_label_update_no_login(client, test_label):
    update_url = urls.reverse("update_label", kwargs={"pk": test_label.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    updated_status = Label.objects.get(id=test_label.id)
    assert updated_status.name == test_label.name


@pytest.mark.django_db
def test_label_delete(client, test_label, authenticated_user):
    assert Label.objects.filter(id=test_label.id).exists() is True
    delete_url = urls.reverse("delete_label", kwargs={"pk": test_label.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("labels")
    assert Label.objects.filter(id=test_label.id).exists() is False


@pytest.mark.django_db
def test_label_delete_no_login(client, test_label):
    delete_url = urls.reverse("delete_label", kwargs={"pk": test_label.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    assert Label.objects.filter(id=test_label.id).exists() is True


@pytest.mark.django_db
def test_label_in_task_delete(client, test_task, authenticated_user):
    test_label = test_task.labels.all()[0]
    delete_url = urls.reverse("delete_label", kwargs={"pk": test_label.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("labels")
    assert Label.objects.filter(id=test_label.id).exists() is True
