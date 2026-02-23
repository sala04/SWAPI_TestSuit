
def test_item_out(app):
    app.inventory.navigation()
    app.inventory.add_backpack_to_cart()
    assert app.inventory.get_cart_count() == "1"

    app.inventory.check_cart()
    assert "cart.html" in app.page.url

    app.cart.navigation()
    app.cart.remove_item()
    assert app.cart.empty_cart_count()

def test_go_back(app):
    app.inventory.navigation()
    app.inventory.add_backpack_to_cart()
    assert app.inventory.get_cart_count() == "1"

    app.inventory.check_cart()
    assert "cart.html" in app.page.url

    app.cart.navigation()
    app.cart.continue_shopping()
    assert "inventory.html" in app.page.url

def test_go_checkout(app):
    app.inventory.navigation()
    app.inventory.add_backpack_to_cart()
    assert app.inventory.get_cart_count() == "1"

    app.inventory.check_cart()
    assert "cart.html" in app.page.url

    app.cart.navigation()
    app.cart.check_out()

    assert "checkout-step-one.html" in app.page.url