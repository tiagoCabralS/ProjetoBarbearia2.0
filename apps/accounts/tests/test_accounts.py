import pytest
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_normalizes_email_and_hashes_password():
    user = User.objects.create_user(email="Ana@Exemplo.COM", password="s3nha-forte", name="Ana")
    assert user.email == "ana@exemplo.com"
    assert user.password != "s3nha-forte"
    assert user.check_password("s3nha-forte")


@pytest.mark.django_db
def test_login_by_email():
    User.objects.create_user(email="ana@exemplo.com", password="s3nha-forte", name="Ana")
    assert authenticate(username="ana@exemplo.com", password="s3nha-forte") is not None


@pytest.mark.django_db
def test_email_is_required():
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="x", name="Sem e-mail")


@pytest.mark.django_db
def test_superuser_flags():
    admin = User.objects.create_superuser(email="root@exemplo.com", password="x", name="Root")
    assert admin.is_staff and admin.is_superuser
