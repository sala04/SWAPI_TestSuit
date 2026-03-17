from playwright.sync_api import Page


class SauceDemoCheckoutStepOnePage:

    URL = "https://www.saucedemo.com/checkout-step-one.html"
    TITLE = "Checkout: Your Information"

    def __init__(self, page: Page):
        self.page = page

        #title
        self.page_title = page.locator('data-test=title')

        #input fields
        self.first_name_input = page.locator('data-test=firstName')
        self.last_name_input = page.locator('data-test=lastName')
        self.postal_code_input = page.locator('data-test=postalCode')

        #buttons
        self.cancel_button = page.locator('data-test=cancel')
        self.continue_button = page.locator('data-test=continue')

        #errors
        self.error_first_name_required = page.locator(
            'data-test=error',
            has_text="Error: First Name is required"
        )

        self.error_last_name_required = page.locator(
            'data-test=error',
            has_text="Error: Last Name is required"
        )

        self.error_postal_code_required = page.locator(
            'data-test=error',
            has_text="Error: Postal Code is required"
        )

    def get_title_name(self) -> str:
        return self.page_title.text_content()

    def fill_checkout_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def cancel_checkout(self) -> None:
        self.cancel_button.click()

    def continue_checkout(self) -> None:
        self.continue_button.click()

    def is_first_name_error_visible(self) -> bool:
        return self.error_first_name_required.is_visible()

    def is_last_name_error_visible(self) -> bool:
        return self.error_last_name_required.is_visible()

    def is_postal_code_error_visible(self) -> bool:
        return self.error_postal_code_required.is_visible()