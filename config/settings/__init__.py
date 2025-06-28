import os

env = os.environ.get("DJANGO_ENV", "dev")  # fallback su 'dev'
if env == "prod":
    from .production import *
else:
    from .development import *