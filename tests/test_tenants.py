import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.tenants.models import Establishment, Membership


@pytest.fixture
def estab(db):
    return Establishment.objects.create(name="Salão Aurora", slug="salao-aurora")


@pytest.mark.django_db
def test_slug_must_be_unique(estab):
    with pytest.raises(IntegrityError):
        Establishment.objects.create(name="Outro", slug="salao-aurora")


@pytest.mark.django_db
def test_slug_is_lowercased():
    e = Establishment.objects.create(name="X", slug="MeuSalao")
    assert e.slug == "meusalao"


@pytest.mark.django_db
def test_reserved_slug_is_rejected():
    e = Establishment(name="Admin", slug="admin")
    with pytest.raises(ValidationError):
        e.full_clean()


@pytest.mark.django_db
def test_user_can_have_roles_in_many_establishments(user, estab):
    outro = Establishment.objects.create(name="Clínica Sol", slug="clinica-sol")
    Membership.objects.create(user=user, establishment=estab, role=Membership.Role.ADMIN)
    Membership.objects.create(user=user, establishment=outro, role=Membership.Role.CLIENT)
    assert user.memberships.count() == 2


@pytest.mark.django_db
def test_same_role_twice_in_same_establishment_is_blocked(user, estab):
    Membership.objects.create(user=user, establishment=estab, role=Membership.Role.ADMIN)
    with pytest.raises(IntegrityError):
        Membership.objects.create(user=user, establishment=estab, role=Membership.Role.ADMIN)


@pytest.mark.django_db
def test_admin_can_also_be_provider(user, estab):
    Membership.objects.create(user=user, establishment=estab, role=Membership.Role.ADMIN)
    Membership.objects.create(user=user, establishment=estab, role=Membership.Role.PROVIDER)
    assert user.memberships.filter(establishment=estab).count() == 2