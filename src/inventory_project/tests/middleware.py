import os
import sys

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def _print_and_message(request, msg, level=messages.WARNING):
    print(f' *** {msg} ***', file=sys.stderr)
    messages.add_message(request, level, msg)


class AlwaysLoggedInAsSuperUser:
    """
    Auto login all users as default superuser.
    Default user will be created, if not exist.

    Disable it by deactivate the default user.
    """

    def __init__(self, get_response):
        assert 'RUN_MAIN' in os.environ, 'Only allowed running by Django dev. server !'
        self.get_response = get_response

    def __call__(self, request):
        self._auto_login(request)
        response = self.get_response(request)

        return response

    def _auto_login(self, request):
        if request.user.is_authenticated:
            return

        try:
            user = User.objects.get(username=settings.DEFAULT_USERNAME)
        except User.DoesNotExist:
            _print_and_message(request, f'Create test django user: {settings.DEFAULT_USERNAME!r}')
            User.objects.create_superuser(
                username=settings.DEFAULT_USERNAME,
                email=settings.DEFAULT_USEREMAIL,
                password=settings.DEFAULT_USERPASS
            )
        else:
            if not user.is_active:
                _print_and_message(request, 'Default User was deactivated!', level=messages.ERROR)
                return

            user.set_password(settings.DEFAULT_USERPASS)
            user.save()

        _print_and_message(
            request,
            f'Autologin applied. Your logged in as {settings.DEFAULT_USERNAME!r}'
        )
        user = authenticate(
            request=request,
            username=settings.DEFAULT_USERNAME,
            password=settings.DEFAULT_USERPASS
        )
        login(request, user)
