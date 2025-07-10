import os
from .base import *

DEBUG = True
SECRET_KEY="secret-key"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'engine': 'django.db.backends.sqlite3',
        'name': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CORS_ALLOW_ALL_ORIGINS = True