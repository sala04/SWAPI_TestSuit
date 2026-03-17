import pytest

from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.item_detail import SauceDemoItemDetailPage
from pages.cart import SauceDemoCartPage
from pages.checkout_step_one import SauceDemoCheckoutStepOnePage
from pages.checkout_step_two import SauceDemoCheckoutStepTwoPage
from pages.checkout_complete import SauceDemoCheckoutComplete
from playwright.sync_api import Page

@pytest.fixture
def login_page(page: Page) -> SauceDemoLoginPage:
    return SauceDemoLoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> SauceDemoInventoryPage:
    return SauceDemoInventoryPage(page)

@pytest.fixture
def item_detail_page(page: Page) -> SauceDemoItemDetailPage:
    return SauceDemoItemDetailPage(page)

@pytest.fixture
def cart_page(page: Page) -> SauceDemoCartPage:
    return SauceDemoCartPage(page)

@pytest.fixture
def checkout_step_one_page(page: Page) -> SauceDemoCheckoutStepOnePage:
    return SauceDemoCheckoutStepOnePage(page)

@pytest.fixture
def checkout_step_two_page(page: Page) -> SauceDemoCheckoutStepTwoPage:
    return SauceDemoCheckoutStepTwoPage(page)

@pytest.fixture
def checkout_complete_page(page: Page) -> SauceDemoCheckoutComplete:
    return SauceDemoCheckoutComplete(page)