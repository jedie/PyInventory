from bx_django_utils.test_utils.playwright import PlaywrightTestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import override_settings
from override_storage import locmem_stats_override_storage
from playwright.sync_api import BrowserContext, expect

from inventory import __version__
from inventory.models import ItemImageModel, ItemLinkModel, ItemModel
from inventory_project.tests.fixtures import TempImageFile, get_normal_user
from inventory_project.tests.playwright_utils import login


@override_settings(SECURE_SSL_REDIRECT=False)
class PlaywrightInventoryTestCase(PlaywrightTestCase):
    def test_root_page(self):
        context: BrowserContext = self.browser.new_context(
            ignore_https_errors=True,
            locale='en_US',
            timezone_id='Europe/Berlin',
        )
        with context.new_page() as page:
            page.goto(self.live_server_url)
            expect(page).to_have_url(f'{self.live_server_url}/admin/login/?next=/admin/')
            expect(page).to_have_title(f'Log in | PyInventory v{__version__}')

    def test_login(self):
        username = 'a-user'
        password = 'ThisIsNotAPassword!'
        superuser = User.objects.create_superuser(username=username, password=password)
        superuser.full_clean()

        user = authenticate(request=HttpRequest(), username=username, password=password)
        assert isinstance(user, User)

        context: BrowserContext = self.browser.new_context(
            ignore_https_errors=True,
            locale='en_US',
            timezone_id='Europe/Berlin',
        )
        with context.new_page() as page:
            page.goto(self.live_server_url)
            expect(page).to_have_url(f'{self.live_server_url}/admin/login/?next=/admin/')
            expect(page).to_have_title(f'Log in | PyInventory v{__version__}')

            page.type('#id_username', username)
            page.type('#id_password', password)
            page.locator('text=Log in').click()

            expect(page).to_have_url(f'{self.live_server_url}/admin/')
            expect(page).to_have_title(f'Site administration | PyInventory v{__version__}')

    def test_admin(self):
        superuser = User.objects.create_superuser(username='foo', password='ThisIsNotAPassword!')
        superuser.full_clean()

        context: BrowserContext = self.browser.new_context(
            ignore_https_errors=True,
            locale='en_US',
            timezone_id='Europe/Berlin',
        )
        with context.new_page() as page:
            login(page, self.client, url=self.live_server_url, user=superuser)

            page.goto(f'{self.live_server_url}/admin/')
            expect(page).to_have_url(f'{self.live_server_url}/admin/')
            expect(page).to_have_title(f'Site administration | PyInventory v{__version__}')

    def test_normal_user_create_item(self):
        normal_user = get_normal_user()

        context: BrowserContext = self.browser.new_context(
            ignore_https_errors=True,
            locale='en_US',
            timezone_id='Europe/Berlin',
        )
        with context.new_page() as page, TempImageFile(
            format='png', size=(1, 1)
        ) as png_image, locmem_stats_override_storage() as storage_stats:
            login(page, self.client, url=self.live_server_url, user=normal_user)

            page.goto(f'{self.live_server_url}/admin/inventory/itemmodel/add/')
            expect(page).to_have_title(f'Add Item | PyInventory v{__version__}')

            page.locator('label:has-text("Kind:")')
            kind_field = page.locator('//input[@id="id_kind"]/..//input[@role="searchbox"]')
            kind_field.click()
            kind_field.fill('Mainboard')
            kind_field.press('Enter')

            page.locator('label:has-text("Producer:")')
            producer_field = page.locator('//input[@id="id_producer"]/..//input[@role="searchbox"]')
            producer_field.click()
            producer_field.fill('Triple D Int.Ltd.')
            producer_field.press('Enter')

            page.locator('label:has-text("Name:")')
            page.fill('//input[@id="id_name"]', 'TD-20 (8088)')

            # Add a Link:
            page.get_by_role('link', name='Add another Link').click()
            page.locator('#id_itemlinkmodel_set-0-url').click()
            page.locator('#id_itemlinkmodel_set-0-url').fill('http://test.tld/foo/bar')
            page.locator('#id_itemlinkmodel_set-0-name').click()
            page.locator('#id_itemlinkmodel_set-0-name').fill('The First Link')
            page.locator('#id_itemlinkmodel_set-0-tags').click()
            page.locator('#id_itemlinkmodel_set-0-tags').fill('a-link-tag')
            page.locator('#id_itemlinkmodel_set-0-tags').press('Tab')

            # Add Image
            page.get_by_role('link', name='Add another Image').click()
            page.locator('#id_itemimagemodel_set-0-image').click()
            page.locator('#id_itemimagemodel_set-0-image').set_input_files(png_image.name)
            page.locator('#id_itemimagemodel_set-0-name').click()
            page.locator('#id_itemimagemodel_set-0-name').fill('The Image Name')
            page.locator('#id_itemimagemodel_set-0-tags').click()
            page.locator('#id_itemimagemodel_set-0-tags').fill('a-image-tag')
            page.locator('#id_itemimagemodel_set-0-tags').press('Tab')

            assert ItemModel.objects.count() == 0

            # Save the item:
            page.locator('input:has-text("Save and continue editing")').click()
            page.locator('text=The Tunes Item “A Test Tunes Item” was added successfully. You may edit it again')
            page.locator('text="Triple D Int.Ltd." - TD-20 (8088)')

            assert ItemModel.objects.count() == 1
            item = ItemModel.objects.first()
            assert item.verbose_name() == 'Mainboard - "Triple D Int.Ltd." - TD-20 (8088)'

            # Save & continue?
            expect(page).to_have_url(f'{self.live_server_url}/admin/inventory/itemmodel/{item.id}/change/')

            # Check added image:
            page.locator('text=The Image Name')
            img = page.locator('//a[@class="image_file_input_preview"]/img')
            img.scroll_into_view_if_needed()
            img.is_visible()
            assert img.evaluate('image => image.complete') is True

            assert item.itemimagemodel_set.count() == 1
            image: ItemImageModel = item.itemimagemodel_set.first()
            assert str(image) == 'The Image Name'
            assert image.user == normal_user
            assert image.tags.get_tag_list() == ['a-image-tag']

            # Check the added link:
            page.locator('text=The First Link')
            page.locator('text=Currently: http://test.tld/foo/bar')
            links = list(item.itemlinkmodel_set.values_list('name', 'url'))
            assert links == [('The First Link', 'http://test.tld/foo/bar')]
            link: ItemLinkModel = item.itemlinkmodel_set.first()
            assert link.tags.get_tag_list() == ['a-link-tag']

            # The "png_image" file should be stored:
            self.assertEqual(storage_stats.save_cnt, 1)
