from playwright.sync_api import Page

class SauceDemoLoginPage:

    URL = 'https://www.saucedemo.com/'

    def __init__(self, page: Page):
        self.page = page

        #fields
        self.username = page.locator('id=user-name')
        self.password = page.locator('id=password')

        #buttons
        self.login_button = page.locator('id=login-button')

        #messages
        self.wrong_credentials_text = page.locator('data-test=error',
                                                   has_text='Epic sadface: Username and password do not match any user in this service')
        self.locked_out_user_text = page.locator('data-test=error',
                                                   has_text='Epic sadface: Sorry, this user has been locked out.')
        self.no_username_text = page.locator('data-test=error',
                                                 has_text='Epic sadface: Username is required')
        self.no_password_text = page.locator('data-test=error',
                                                 has_text='Epic sadface: Password is required')

    def load(self) -> None:
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()