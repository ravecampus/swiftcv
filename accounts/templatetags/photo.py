import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def profile_pic_url(photo):
    if photo:
        return os.path.join(settings.MEDIA_URL, photo.url)