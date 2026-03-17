from pathlib import Path
import json
import pytest

from playwright.sync_api import Page, expect
from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.item_detail import SauceDemoItemDetailPage

auth_path = (Path(__file__).parent.parent / 'test_data' / 'auth.json').resolve()
with auth_path.open('r', encoding='utf-8') as f:
    auth_data = json.load(f)

usernames_ok = auth_data['usernames_ok']


@pytest.fixture(scope='function', autouse=True)
def inventory_module_setup(
        username: str,
        page: Page,
        login_page: SauceDemoLoginPage,
        inventory_page: SauceDemoInventoryPage):
    login_page.load()
    login_page.login(username=username, password=auth_data['password'])
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()

    return inventory_page


@pytest.mark.parametrize('username', usernames_ok)
def test_logout(inventory_page: SauceDemoInventoryPage, login_page: SauceDemoLoginPage, page: Page):
    inventory_page.logout()
    expect(page).to_have_url(login_page.URL, timeout=1500)
    expect(login_page.username).to_be_visible()


@pytest.mark.parametrize('username', usernames_ok)
def test_inventory_items_present(inventory_page: SauceDemoInventoryPage):
    assert inventory_page.get_inventory_count() > 0


@pytest.mark.parametrize('username', usernames_ok)
def test_consistency(inventory_page: SauceDemoInventoryPage):
    # save initial value
    initial_names = inventory_page.get_product_names()
    initial_prices = inventory_page.get_product_prices()
    initial_count = inventory_page.get_inventory_count()

    # reload
    inventory_page.page.reload()
    expect(inventory_page.inventory_container).to_be_visible()

    # save new state
    new_names = inventory_page.get_product_names()
    new_prices = inventory_page.get_product_prices()
    new_count = inventory_page.get_inventory_count()

    assert initial_count == new_count
    assert initial_names == new_names
    assert initial_prices == new_prices


@pytest.mark.parametrize('username', usernames_ok)
def test_unique_items(inventory_page: SauceDemoInventoryPage):
    srcs = inventory_page.get_all_product_image_sources()
    assert srcs, "No images found"
    assert len(srcs) == len(set(srcs)), "There are duplicated images"


sort_values = [
    "az",
    "za",
    "lohi",
    "hilo"
]


@pytest.mark.parametrize("username", usernames_ok)  # para ahorrar tiempo
@pytest.mark.parametrize("sort_value", sort_values)
def test_sort(
        inventory_page: SauceDemoInventoryPage,
        sort_value
):
    inventory_page.sort_by(sort_value)
    product_names = inventory_page.get_product_names()
    product_prices = inventory_page.get_product_prices()
    if sort_value == 'az':
        assert product_names == sorted(product_names)
    elif sort_value == 'za':
        assert product_names == sorted(product_names, reverse=True)
    elif sort_value == 'lohi':
        assert product_prices == sorted(product_prices)
    elif sort_value == 'hilo':
        assert product_prices == sorted(product_prices, reverse=True)


@pytest.mark.parametrize("username", usernames_ok)
def test_add_remove_items(inventory_page: SauceDemoInventoryPage):
    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    assert inventory_page.is_add_button_visible(product_names[0]) is False
    assert inventory_page.is_remove_button_visible(product_names[0]) is True
    assert inventory_page.get_cart_badge_count() == 1

    inventory_page.click_product_to_cart_by_name(product_names[1])
    assert inventory_page.is_add_button_visible(product_names[1]) is False
    assert inventory_page.is_remove_button_visible(product_names[1]) is True
    assert inventory_page.get_cart_badge_count() == 2

    inventory_page.click_product_to_cart_by_name(product_names[4])
    assert inventory_page.is_add_button_visible(product_names[4]) is False
    assert inventory_page.is_remove_button_visible(product_names[4]) is True
    assert inventory_page.get_cart_badge_count() == 3

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[4])
    assert inventory_page.is_add_button_visible(product_names[0]) is True
    assert inventory_page.is_add_button_visible(product_names[1]) is True
    assert inventory_page.is_add_button_visible(product_names[4]) is True
    assert inventory_page.get_cart_badge_count() == 0


@pytest.mark.parametrize("username", usernames_ok)
def test_navigate_to_detailed_view(inventory_page: SauceDemoInventoryPage, item_detail_page: SauceDemoItemDetailPage,
                                   page: Page):
    product_names = inventory_page.get_product_names()
    inventory_page.click_detail_view(product_names[0])

    expect(item_detail_page.product_name).to_be_visible()
    assert item_detail_page.get_product_name() == product_names[0]

    item_detail_page.go_back_to_products()
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()