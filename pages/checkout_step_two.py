from playwright.sync_api import Page


class SauceDemoCheckoutStepTwoPage:

    URL = "https://www.saucedemo.com/checkout-step-two.html"
    TITLE = "Checkout: Overview"

    def __init__(self, page: Page):
        self.page = page

        #prices
        self.item_prices = page.locator('data-test=inventory-item-price')

        #title
        self.page_title = page.locator('data-test=title')

        #summary info
        self.item_total_label = page.locator('data-test=subtotal-label')
        self.tax_label = page.locator('data-test=tax-label')
        self.total_label = page.locator('data-test=total-label')

        #buttons
        self.cancel_button = page.locator('data-test=cancel')
        self.finish_button = page.locator('data-test=finish')

    def get_title_name(self) -> str:
        return self.page_title.text_content()

    def get_product_prices(self) -> list[float]:
        prices = self.item_prices.all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def get_item_total(self) -> float:
        text = self.item_total_label.text_content()
        return float(text.split("$")[1]) #get second half

    def get_tax(self) -> float:
        text = self.tax_label.text_content()
        return float(text.split("$")[1]) #get second half

    def get_total(self) -> float:
        text = self.total_label.text_content()
        return float(text.split("$")[1]) #get second half

    def cancel(self) -> None:
        self.cancel_button.click()

    def finish_checkout(self) -> None:
        self.finish_button.click()