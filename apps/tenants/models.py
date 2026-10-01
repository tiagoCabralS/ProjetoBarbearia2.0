from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Slugs que colidem com rotas do sistema (a página pública usa /{slug})
RESERVED_SLUGS = {
    "admin", "api", "app", "login", "logout", "register", "cadastro",
    "static", "media", "docs", "health", "painel", "www",
}

def validate_slug_not_reserved(value):
    if value.lower() in RESERVED_SLUGS:
        raise ValidationError("Este endereço é reservado. Escolha outro.")

class Establishment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Ativo"
        SUSPENDED = "SUSPENDED", "Suspenso"
    
    name = models.CharField("nome", max_length=150)
    slug = models.SlugField(
        "endereço (slug)",
        max_length=60,
        unique=True,
        validators=[validate_slug_not_reserved],
        help_text="Usado na página pública: app.com/<slug>",
    )
    timezone = models.CharField("fuso horário", max_length=64, default="America/Sao_Paulo")
    phone = models.CharField("telefone", max_length=20, blank=True)
    address = models.CharField("endereço", max_length=255, blank=True)
    settings_json = models.JSONField("configurações", default=dict, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "estabelecimento"
        verbose_name_plural = "estabelecimentos"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)
    
class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        ATTENDANT = "ATTENDANT", "Atendente"
        PROVIDER = "PROVIDER", "Prestador"
        CLIENT = "CLIENT", "Cliente"
    
    class Status(models.TextChoices):
        INVITED = "INVITED", "Convidado"
        ACTIVE = "ACTIVE", "Ativo"
        INACTIVE = "INACTIVE", "Inativo"
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    establishment = models.ForeignKey(
        Establishment, on_delete=models.PROTECT, related_name="memberships"
    )
    role = models.CharField(max_length=12, choices=Role.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "vínculo"
        verbose_name_plural = "vínculos"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "establishment", "role"],
                name="uniq_membership_user_establishment_role",
            )
        ]
        indexes = [models.Index(fields=["establishment", "role", "status"])]

    def __str__(self):
        return f"{self.user} @ {self.establishment} ({self.role})"