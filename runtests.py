#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.core.management import call_command
from django.test.utils import get_runner

SETTINGS = {
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    "INSTALLED_APPS": (
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "doorkeeper",
        "doorkeeper.tests.test_app",
    ),
    "SECRET_KEY": "testing",
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                ]
            },
        }
    ],
    "MIDDLEWARE": (
        "doorkeeper.middleware.DoorkeeperMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ),
    "DOORKEEPER": {
        "ENABLED": True,
        "PASSWORD": "sesame",
        "DEFAULT_REDIRECT_URL": "/",
    },
    "ROOT_URLCONF": "doorkeeper.tests.urls",
}


if not settings.configured:
    settings.configure(**SETTINGS)


def runtests():
    django.setup()

    failures = call_command(
        "test",
        *sys.argv[1:] if len(sys.argv) > 1 else ["doorkeeper"],
        interactive=False,
        failfast=False,
        verbosity=1,
    )

    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests()
