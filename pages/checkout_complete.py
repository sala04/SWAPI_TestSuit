from playwright.sync_api import Page

class SauceDemoCheckoutComplete:

    URL = "https://www.saucedemo.com/checkout-complete.html"
    TITLE = "Checkout: Complete!"
    HEADER = "Thank you for your order!"

    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.locator('data-test=title')
        self.header = page.locator('data-test=complete-header')
        self.back_home_button = page.locator('data-test=back-to-products')

    def get_title_name(self) -> str:
        return self.page_title.text_content()

    def get_header_name(self) -> str:
        return self.header.text_content()

    def go_back_home(self) -> None:
        self.back_home_button.click()