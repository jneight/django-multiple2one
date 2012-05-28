# coding=utf-8

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from django.db.models import Q
from django.db.models import get_model
from middleware import get_current_site


class SiteBackend(ModelBackend):
    def authenticate(self, **credentials):
        try:
            user = self.user_class.objects.get(Q(is_superuser=True) | Q(site = get_current_site()), username=credentials['username'], )
            is_valid = user.check_password(credentials['password'])
            if is_valid:
                return user
        except:
            pass
        return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class