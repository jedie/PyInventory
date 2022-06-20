import pytest
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from playwright.sync_api import Page, expect

from inventory import __version__
from inventory_project.tests.playwright_utils import login


@pytest.mark.playwright
def test_root_page(live_server, page: Page):
    # https://github.com/microsoft/playwright-pytest/issues/115
    assert settings.SECURE_SSL_REDIRECT is False

    page.goto(live_server.url)
    expect(page).to_have_url(f'{live_server}/admin/login/?next=/admin/')
    expect(page).to_have_title(f'Log in | PyInventory v{__version__}')


@pytest.mark.playwright
def test_login(live_server, page: Page):
    username = 'a-user'
    password = 'ThisIsNotAPassword!'
    superuser = User.objects.create_superuser(username=username, password=password)
    superuser.full_clean()

    user = authenticate(request=HttpRequest(), username=username, password=password)
    assert isinstance(user, User)

    page.goto(live_server.url)
    expect(page).to_have_url(f'{live_server}/admin/login/?next=/admin/')
    expect(page).to_have_title(f'Log in | PyInventory v{__version__}')

    page.type('#id_username', username)
    page.type('#id_password', password)
    page.locator('text=Log in').click()

    expect(page).to_have_url(f'{live_server}/admin/')
    expect(page).to_have_title(f'Site administration | PyInventory v{__version__}')


@pytest.mark.playwright
def test_admin(live_server, client, page: Page):
    superuser = User.objects.create_superuser(username='foo', password='ThisIsNotAPassword!')
    superuser.full_clean()
    login(page, client, url=live_server.url, user=superuser)

    page.goto(f'{live_server}/admin/')
    expect(page).to_have_url(f'{live_server}/admin/')
    expect(page).to_have_title(f'Site administration | PyInventory v{__version__}')
