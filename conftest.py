import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture
def app(page):
    login = LoginPage(page)
    login.navigation()
    login.login("standard_user", "secret_sauce")

    class App:
        def __init__(self):
            self.login = LoginPage(page)
            self.inventory = InventoryPage(page)
            self.cart = CartPage(page)
            self.page = page  # Por si necesitas la URL o screenshots

    return App()

@pytest.fixture(scope="session")
def api_request_context():
    """
    Crea un contexto de peticiones para API.
    'scope="session"' significa que se crea una vez para todos los tests,
    lo que lo hace mucho más rápido.
    """
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url="https://swapi.dev/api/"
        )
        yield request_context
        request_context.dispose()