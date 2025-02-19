from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static
from django.utils import timezone

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'settings': settings,
        'now': timezone.now,
    })
    return env
