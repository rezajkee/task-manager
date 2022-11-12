import pytest
from django import urls
from task_manager.tags.models import Tag


@pytest.mark.django_db
@pytest.mark.parametrize("param", [("tags"), ("create_tag")])
def test_render_views(client, authenticated_user, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_tag_creation(client, authenticated_user):
    assert Tag.objects.count() == 0
    creation_url = urls.reverse("create_tag")
    resp = client.post(creation_url, {"name": "first"})
    assert Tag.objects.count() == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_tag_creation_no_login(client):
    assert Tag.objects.count() == 0
    creation_url = urls.reverse("create_tag")
    resp = client.post(creation_url, {"name": "first"})
    assert Tag.objects.count() == 0
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")


@pytest.mark.django_db
def test_tag_update(client, test_tag, authenticated_user):
    update_url = urls.reverse("update_tag", kwargs={"pk": test_tag.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tags")
    updated_tag = Tag.objects.get(id=test_tag.id)
    assert updated_tag.name == "not a test"


@pytest.mark.django_db
def test_tag_update_no_login(client, test_tag):
    update_url = urls.reverse("update_tag", kwargs={"pk": test_tag.id})
    resp = client.post(update_url, {"name": "not a test"})
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    updated_status = Tag.objects.get(id=test_tag.id)
    assert updated_status.name == test_tag.name


@pytest.mark.django_db
def test_tag_delete(client, test_tag, authenticated_user):
    assert Tag.objects.filter(id=test_tag.id).exists() is True
    delete_url = urls.reverse("delete_tag", kwargs={"pk": test_tag.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tags")
    assert Tag.objects.filter(id=test_tag.id).exists() is False


@pytest.mark.django_db
def test_tag_delete_no_login(client, test_tag):
    delete_url = urls.reverse("delete_tag", kwargs={"pk": test_tag.id})
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    assert Tag.objects.filter(id=test_tag.id).exists() is True


@pytest.mark.django_db
def test_tag_in_task_delete(client, test_task, authenticated_user):
    delete_url = urls.reverse(
        "delete_tag", kwargs={"pk": test_task.tags.id}
    )
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("tags")
    assert Tag.objects.filter(id=test_task.tag.id).exists() is True
