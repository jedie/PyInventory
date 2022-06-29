import pytest
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from playwright.sync_api import Page, expect

from inventory import __version__
from inventory.models import ItemImageModel, ItemLinkModel, ItemModel
from inventory_project.tests.fixtures import get_normal_user
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


@pytest.mark.playwright
def test_normal_user_create_item(live_server, client, page: Page, png_image):
    normal_user = get_normal_user()
    login(page, client, url=live_server.url, user=normal_user)

    page.goto(f'{live_server}/admin/inventory/itemmodel/add/')
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
    page.locator('text=Add another Link').click()
    link_tags = page.locator(
        '//input[@id="id_itemlinkmodel_set-0-tags"]/..//input[@role="searchbox"]'
    )
    link_tags.click()
    link_tags.fill('a-link-tag')
    link_tags.press('Enter')
    page.locator('input[name="itemlinkmodel_set-0-name"]').fill('The First Link')
    page.locator('input[name="itemlinkmodel_set-0-url"]').fill('http://test.tld/foo/bar')

    # Add Image
    page.locator("text=Add another Image").click()
    choose_file = page.locator("input[name=\"itemimagemodel_set-0-image\"]")
    choose_file.set_input_files(png_image.name)
    page.fill("input[name=\"itemimagemodel_set-0-name\"]", "The Image Name")
    image_tags = page.locator(
        '//input[@id="id_itemimagemodel_set-0-tags"]/..//input[@role="searchbox"]'
    )
    image_tags.click()
    image_tags.fill('a-image-tag')
    image_tags.press("Enter")

    assert ItemModel.objects.count() == 0

    # Save the item:
    page.locator('input:has-text("Save and continue editing")').click()
    page.locator(
        'text=The Tunes Item “A Test Tunes Item” was added successfully. You may edit it again'
    )
    page.locator('text="Triple D Int.Ltd." - TD-20 (8088)')

    assert ItemModel.objects.count() == 1
    item = ItemModel.objects.first()
    assert item.verbose_name() == 'Mainboard - "Triple D Int.Ltd." - TD-20 (8088)'

    # Save & continue?
    expect(page).to_have_url(f'{live_server}/admin/inventory/itemmodel/{item.id}/change/')

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
