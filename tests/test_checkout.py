from pathlib import Path
import json
import pytest

from playwright.sync_api import Page, expect
from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.cart import SauceDemoCartPage
from pages.checkout_step_one import SauceDemoCheckoutStepOnePage
from pages.checkout_step_two import SauceDemoCheckoutStepTwoPage
from pages.checkout_complete import SauceDemoCheckoutComplete
from tests.conftest import checkout_step_one_page

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
        cart_page: SauceDemoCartPage,
        checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    login_page.load()
    login_page.login(username=username, password=auth_data['password'])
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()

    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[5])

    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

    #check all products are in cart
    assert cart_page.get_cart_count() == 3
    products_in_cart = cart_page.get_product_names()
    assert product_names[0] in products_in_cart
    assert product_names[1] in products_in_cart
    assert product_names[5] in products_in_cart


    cart_page.proceed_to_checkout()
    assert checkout_step_one_page.page_title.is_visible()
    assert checkout_step_one_page.get_title_name() == checkout_step_one_page.TITLE

    return checkout_step_one_page

@pytest.mark.parametrize("username", usernames_ok)
def test_cancel(checkout_step_one_page: SauceDemoCheckoutStepOnePage, cart_page: SauceDemoCartPage):

    checkout_step_one_page.cancel_checkout()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

@pytest.mark.parametrize("username", usernames_ok)
def test_empty_form(checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.error_first_name_required).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_empty_username(checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    checkout_step_one_page.fill_checkout_information(first_name='', last_name='last_name', postal_code='postal_code')
    checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.error_first_name_required).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_empty_last_name(checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    checkout_step_one_page.fill_checkout_information(first_name='first_name', last_name='', postal_code='postal_code')
    checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.error_last_name_required).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_empty_postal_code(checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    checkout_step_one_page.fill_checkout_information(first_name='first_name', last_name='last_name', postal_code='')
    checkout_step_one_page.continue_checkout()
    expect(checkout_step_one_page.error_postal_code_required).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_total_amount_is_correct(checkout_step_one_page: SauceDemoCheckoutStepOnePage, checkout_step_two_page: SauceDemoCheckoutStepTwoPage):

    checkout_step_one_page.fill_checkout_information(first_name='first_name', last_name='last_name', postal_code='postal_code')
    checkout_step_one_page.continue_checkout()

    assert checkout_step_two_page.page_title.is_visible()
    assert checkout_step_two_page.get_title_name() == checkout_step_two_page.TITLE

    item_prices_total = sum(checkout_step_two_page.get_product_prices())
    assert item_prices_total == checkout_step_two_page.get_item_total()
    assert checkout_step_two_page.get_total() == checkout_step_two_page.get_item_total() + checkout_step_two_page.get_tax()

@pytest.mark.parametrize("username", usernames_ok)
def test_cancel_in_second_checkout_screen(
        checkout_step_one_page: SauceDemoCheckoutStepOnePage,
        checkout_step_two_page: SauceDemoCheckoutStepTwoPage,
        inventory_page: SauceDemoInventoryPage,
        page: Page):

    checkout_step_one_page.fill_checkout_information(first_name='first_name', last_name='last_name', postal_code='postal_code')
    checkout_step_one_page.continue_checkout()

    assert checkout_step_two_page.page_title.is_visible()
    assert checkout_step_two_page.get_title_name() == checkout_step_two_page.TITLE

    checkout_step_two_page.cancel()
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_complete_checkout_flow(
        checkout_step_one_page: SauceDemoCheckoutStepOnePage,
        checkout_step_two_page: SauceDemoCheckoutStepTwoPage,
        checkout_complete_page: SauceDemoCheckoutComplete,
        inventory_page: SauceDemoInventoryPage,
        page: Page):


    checkout_step_one_page.fill_checkout_information(first_name='first_name', last_name='last_name', postal_code='postal_code')
    checkout_step_one_page.continue_checkout()

    assert checkout_step_two_page.page_title.is_visible()
    assert checkout_step_two_page.get_title_name() == checkout_step_two_page.TITLE

    checkout_step_two_page.finish_checkout()
    assert checkout_complete_page.page_title.is_visible()
    assert checkout_complete_page.get_title_name() == checkout_complete_page.TITLE
    assert checkout_complete_page.get_header_name() == checkout_complete_page.HEADER

    checkout_complete_page.go_back_home()
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()