from pathlib import Path
import json
import pytest

from playwright.sync_api import Page, expect
from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage

auth_path = (Path(__file__).parent.parent / 'test_data' / 'auth.json').resolve()
with auth_path.open('r', encoding='utf-8') as f:
    auth_data = json.load(f)


usernames_ok = auth_data['usernames_ok']

@pytest.mark.parametrize('username', usernames_ok, ids=usernames_ok)
def test_login_ok(
        username: str,
        page: Page,
        login_page: SauceDemoLoginPage,
        inventory_page: SauceDemoInventoryPage) -> None:

    page.set_default_timeout(3000) #to check performance issues
    login_page.load()
    login_page.login(username=username, password=auth_data['password'])
    expect(page).to_have_url(inventory_page.URL, timeout=1500)

def test_login_wrong_password(
        page: Page,
        login_page: SauceDemoLoginPage
        ) -> None:

    login_page.load()
    login_page.login(username=auth_data['usernames_ok'][0], password='wrong_password')
    expect(login_page.wrong_credentials_text).to_be_visible()
    expect(page).to_have_url(login_page.URL, timeout=1500)

def test_login_locked_user(
        page: Page,
        login_page: SauceDemoLoginPage
        ) -> None:

    login_page.load()
    login_page.login(username=auth_data['usernames_ko'][0], password=auth_data['password'])
    expect(login_page.locked_out_user_text).to_be_visible()
    expect(page).to_have_url(login_page.URL, timeout=1500)

def test_login_no_username(
        page: Page,
        login_page: SauceDemoLoginPage
        ) -> None:

    login_page.load()
    login_page.login(username='', password=auth_data['password'])
    expect(login_page.no_username_text).to_be_visible()
    expect(page).to_have_url(login_page.URL, timeout=1500)

def test_login_no_password(
        page: Page,
        login_page: SauceDemoLoginPage
        ) -> None:

    login_page.load()
    login_page.login(username=auth_data['usernames_ok'][0], password='')
    expect(login_page.no_password_text).to_be_visible()
    expect(page).to_have_url(login_page.URL, timeout=1500)

def test_login_no_username_no_password(
        page: Page,
        login_page: SauceDemoLoginPage
        ) -> None:

    login_page.load()
    login_page.login(username='', password='')
    expect(login_page.no_username_text).to_be_visible()
    expect(page).to_have_url(login_page.URL, timeout=1500)