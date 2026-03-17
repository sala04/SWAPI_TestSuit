from playwright.sync_api import Page, expect


class SauceDemoItemDetailPage:

    URL_PATTERN = "**/inventory-item.html*"

    def __init__(self, page: Page):
        self.page = page

        #product info
        self.product_name = page.locator('data-test=inventory-item-name')

        #buttons
        self.add_button = page.locator('data-test=add-to-cart')
        self.remove_button = page.locator('data-test=remove')
        self.back_button = page.locator('data-test=back-to-products')

        #cart
        self.shopping_cart_link = page.locator('data-test=shopping-cart-link')
        self.cart_badge = page.locator('data-test=shopping-cart-badge')



    def go_back_to_products(self) -> None:
        self.back_button.click()

    def get_product_name(self) -> str:
        return self.product_name.text_content()

    def add_to_cart(self) -> None:
        self.add_button.click()

    def remove_from_cart(self) -> None:
        self.remove_button.click()

    def is_add_button_visible(self) -> bool:
        return self.add_button.is_visible()

    def is_remove_button_visible(self) -> bool:
        return self.remove_button.is_visible()

    def get_cart_badge_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content())