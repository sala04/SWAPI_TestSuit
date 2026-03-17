from pathlib import Path
import json
import pytest

from playwright.sync_api import Page, expect
from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.item_detail import SauceDemoItemDetailPage
from tests.conftest import item_detail_page

auth_path = (Path(__file__).parent.parent / 'test_data' / 'auth.json').resolve()
with auth_path.open('r', encoding='utf-8') as f:
    auth_data = json.load(f)


usernames_ok = auth_data['usernames_ok']

@pytest.fixture(scope='function', autouse=True)
def inventory_module_setup(
        username: str,
        page: Page,
        login_page: SauceDemoLoginPage,
        inventory_page: SauceDemoInventoryPage,
        item_detail_page: SauceDemoItemDetailPage):

    login_page.load()
    login_page.login(username=username, password=auth_data['password'])
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()

    product_names = inventory_page.get_product_names()
    inventory_page.click_detail_view(product_names[0])
    expect(item_detail_page.product_name).to_be_visible()
    assert item_detail_page.get_product_name() == product_names[0]

    return item_detail_page

@pytest.mark.parametrize("username", usernames_ok)
def test_add_remove_cart(item_detail_page: SauceDemoItemDetailPage):

    assert item_detail_page.get_cart_badge_count() == 0
    assert item_detail_page.is_add_button_visible() is True
    item_detail_page.add_to_cart()
    assert item_detail_page.is_remove_button_visible() is True
    assert item_detail_page.get_cart_badge_count() == 1

    item_detail_page.remove_from_cart()
    assert item_detail_page.is_add_button_visible() is True
    assert item_detail_page.get_cart_badge_count() == 0