from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import Client
from playwright.sync_api import Page


def login(page: Page, client: Client, url: str, user: User) -> None:
    """
    Helper to fast login, without using the login page.
    """
    # Create a session by using Django's test login:
    client.force_login(user=user)
    session_cookie = client.cookies[settings.SESSION_COOKIE_NAME]
    assert session_cookie

    # Inject the session Cookie to playwright browser:
    cookie_object = {
        'name': session_cookie.key,
        'value': session_cookie.value,
        'url': url,
    }
    page.context.add_cookies([cookie_object])
