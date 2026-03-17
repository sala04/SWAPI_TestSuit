from playwright.sync_api import Page, expect


class SauceDemoCartPage:

    URL = "https://www.saucedemo.com/cart.html"
    TITLE = "Your Cart"

    def __init__(self, page: Page):
        self.page = page

        #items
        self.cart_items = page.locator('data-test=inventory-item')
        self.item_names = page.locator('data-test=inventory-item-name')
        self.inventory_item_prices = page.locator('data-test=inventory-item-price')

        #cart badge
        self.cart_badge = page.locator('data-test=shopping-cart-badge')

        #title header
        self.page_title = page.locator('data-test=title')

        #buttons
        self.continue_shopping_button = page.locator('data-test=continue-shopping')
        self.checkout_button = page.locator('data-test=checkout')

    def get_title_name(self) -> str:
        return self.page_title.text_content()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def get_cart_count(self) -> int:
        return self.cart_items.count()

    def get_product_names(self) -> list[str]:
        return self.item_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices = self.inventory_item_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in prices] #return as float so they can be properly sorted

    def remove_product_by_name(self, product_name: str) -> None:
        item = self.cart_items.filter(has_text=product_name)
        item.get_by_role("button", name="Remove").click()

    def get_cart_badge_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content())