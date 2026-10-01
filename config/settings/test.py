from ..settings import *  # noqa

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # testes mais rápidos
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa
    "DEFAULT_THROTTLE_CLASSES": [],  # evita falhas por rate limit nos testes
}
