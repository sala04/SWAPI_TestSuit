import pytest
from playwright.sync_api import Page, APIRequestContext

URL = "https://swapi.dev/api/"

# Ejemplo de Test de API (Sustituye a Postman)
def test_api_get_user(playwright):
    # Creamos un contexto de API
    api_context = playwright.request.new_context(base_url= URL)
    response = api_context.get("people/1/")

    assert response.ok, f"Error en la petición: {response.status} - {response.url}"

    data =response.json()
    assert data["name"] == "Luke Skywalker"
    assert data["gender"] == "male"
    print("\n✅ API Test pasado con éxito")


# Ejemplo de Test de UI (Playwright + Pytest)
def test_ui_login_navigation(page: Page):
    # Navegación simple
    page.goto("https://www.saucedemo.com/")

    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")

    page.click("#login-button")

    assert "inventory.html" in page.url

    title = page.locator(".title")
    assert title.text_content() == "Products"
    print("✅ UI Test pasado con éxito")


