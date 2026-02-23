#Login page UI test
def test_login_page(app):
    assert "inventory.html" in app.page.url