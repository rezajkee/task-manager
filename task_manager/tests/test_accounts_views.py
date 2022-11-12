import pytest
from django import urls
from django.contrib.auth import get_user_model


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param", [("home"), ("register"), ("login"), ("users")]
)
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_user_registration(client, user_reg_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    reg_url = urls.reverse("register")
    resp = client.post(reg_url, user_reg_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302


@pytest.mark.django_db
def test_user_login(client, create_test_user, user_creation_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 1
    login_url = urls.reverse("login")
    resp = client.post(login_url, data=user_creation_data)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("home")


@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
    logout_url = urls.reverse("logout")
    resp = client.post(logout_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("home")


@pytest.mark.django_db
def test_user_update(client, authenticated_user, user_update_data):
    update_url = urls.reverse(
        "update_user", kwargs={"pk": authenticated_user.id}
    )
    resp = client.post(update_url, data=user_update_data)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("users")
    user_model = get_user_model()
    updated_user = user_model.objects.get(id=authenticated_user.id)
    assert updated_user.username == user_update_data.get("username")


@pytest.mark.django_db
def test_user_update_no_login(client, second_test_user, user_update_data):
    update_url = urls.reverse(
        "update_user", kwargs={"pk": second_test_user.id}
    )
    resp = client.post(update_url, data=user_update_data)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    user_model = get_user_model()
    updated_user = user_model.objects.get(id=second_test_user.id)
    assert updated_user.username != user_update_data.get("username")


@pytest.mark.django_db
def test_user_update_other_user(
    client, authenticated_user, second_test_user, user_update_data
):
    update_url = urls.reverse(
        "update_user", kwargs={"pk": second_test_user.id}
    )
    resp = client.post(update_url, data=user_update_data)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("users")
    user_model = get_user_model()
    updated_user = user_model.objects.get(id=second_test_user.id)
    assert updated_user.username != user_update_data.get("username")


@pytest.mark.django_db
def test_user_delete(client, authenticated_user):
    user_model = get_user_model()
    assert user_model.objects.filter(id=authenticated_user.id).exists() is True
    delete_url = urls.reverse(
        "delete_user", kwargs={"pk": authenticated_user.id}
    )
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("users")
    assert (
        user_model.objects.filter(id=authenticated_user.id).exists() is False
    )


@pytest.mark.django_db
def test_user_delete_no_login(client, second_test_user):
    delete_url = urls.reverse(
        "delete_user", kwargs={"pk": second_test_user.id}
    )
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("login")
    user_model = get_user_model()
    assert user_model.objects.filter(id=second_test_user.id).exists() is True


@pytest.mark.django_db
def test_user_delete_other_user(client, authenticated_user, second_test_user):
    delete_url = urls.reverse(
        "delete_user", kwargs={"pk": second_test_user.id}
    )
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("users")
    user_model = get_user_model()
    assert user_model.objects.filter(id=second_test_user.id).exists() is True


@pytest.mark.django_db
def test_user_in_task_delete(
    client, test_task_by_auth_user, authenticated_user
):
    delete_url = urls.reverse(
        "delete_user", kwargs={"pk": authenticated_user.id}
    )
    resp = client.post(delete_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse("users")
    user_model = get_user_model()
    assert user_model.objects.filter(id=authenticated_user.id).exists() is True
