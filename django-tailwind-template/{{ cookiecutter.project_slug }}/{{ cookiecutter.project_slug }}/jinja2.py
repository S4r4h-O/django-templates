from jinja2 import Environment as JinjaEnvironment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def Environment(**options):
    env = JinjaEnvironment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )
    return env
