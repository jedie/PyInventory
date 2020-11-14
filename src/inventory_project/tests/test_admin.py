import os
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django_processinfo.models import ProcessInfo, SiteStatistics
from django_tools.selenium.chromedriver import chromium_available
from django_tools.selenium.django import (
    SeleniumChromiumStaticLiveServerTestCase,
    SeleniumFirefoxStaticLiveServerTestCase,
)
from django_tools.selenium.geckodriver import firefox_available
from model_bakery import baker

from inventory import __version__
from inventory.permissions import get_or_create_normal_user_group


class AdminAnonymousTests(TestCase):
    """
    Anonymous will be redirected to the login page.
    """

    def test_login_en(self):
        response = self.client.get("/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertRedirects(response, expected_url="/admin/login/?next=/admin/")

    def test_login_de(self):
        response = self.client.get("/admin/", HTTP_ACCEPT_LANGUAGE="de")
        self.assertRedirects(response, expected_url="/admin/login/?next=/admin/")


class ProcessinfoAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = baker.make(
            User, is_staff=True, is_active=True, is_superuser=True
        )
        cls.normaluser = baker.make(
            User, is_staff=True, is_active=True, is_superuser=False
        )
        assert cls.normaluser.user_permissions.count() == 0
        group = get_or_create_normal_user_group()[0]
        cls.normaluser.groups.set([group])

    def test_superuser_access(self):
        self.client.force_login(self.superuser)

        assert SiteStatistics.objects.count() == 0
        assert ProcessInfo.objects.count() == 0

        response = self.client.get('/admin/django_processinfo/sitestatistics/')
        self.assertTemplateUsed(response, 'admin/django_processinfo/change_list.html')

        response = response.content.decode("utf-8")
        self.assertInHTML('<h2>System information</h2>', response)
        self.assertInHTML('<dt>Living processes (current/avg/max)</dt>', response)

        assert SiteStatistics.objects.count() == 1
        assert ProcessInfo.objects.count() == 1

        response = self.client.get('/admin/django_processinfo/processinfo/')
        self.assertTemplateUsed(response, 'admin/django_processinfo/change_list.html')

        response = response.content.decode("utf-8")
        self.assertInHTML('<h2>System information</h2>', response)
        self.assertInHTML('<dt>Living processes (current/avg/max)</dt>', response)

        assert SiteStatistics.objects.count() == 1
        assert ProcessInfo.objects.count() == 1

    def test_normal_user_access(self):
        self.client.force_login(self.normaluser)

        assert SiteStatistics.objects.count() == 0
        assert ProcessInfo.objects.count() == 0

        response = self.client.get('/admin/django_processinfo/sitestatistics/')
        assert response.status_code == 403

        response = self.client.get('/admin/django_processinfo/processinfo/')
        assert response.status_code == 403

        assert SiteStatistics.objects.count() == 1
        assert ProcessInfo.objects.count() == 1


@unittest.skipIf('CI' in os.environ, 'Skip, selenium tests does not work on CI run!')
@unittest.skipUnless(chromium_available(), "Skip because Chromium is not available!")
class AdminChromiumTests(SeleniumChromiumStaticLiveServerTestCase):
    def test_admin_login_page(self):
        self.driver.get(self.live_server_url + "/admin/login/")
        self.assert_equal_page_title(f"Log in | PyInventory v{__version__}")
        self.assert_in_page_source('<form action="/admin/login/" method="post" id="login-form">')
        self.assert_no_javascript_alert()


@unittest.skipIf('CI' in os.environ, 'Skip, selenium tests does not work on CI run!')
@unittest.skipUnless(firefox_available(), "Skip because Firefox is not available!")
class AdminFirefoxTests(SeleniumFirefoxStaticLiveServerTestCase):
    def test_admin_login_page(self):
        self.driver.get(self.live_server_url + "/admin/login/")
        self.assert_equal_page_title(f"Log in | PyInventory v{__version__}")
        self.assert_in_page_source('<form action="/admin/login/" method="post" id="login-form">')
        self.assert_no_javascript_alert()
