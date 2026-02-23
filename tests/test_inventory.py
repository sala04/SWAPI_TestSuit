
def test_add_inventory(app):
    app.inventory.navigation()
    app.inventory.add_backpack_to_cart()

    assert app.inventory.get_cart_count() == "1"

    app.inventory.check_cart()
    assert "cart.html" in app.page.url

def test_filter_lohi(app):
    app.inventory.apply_filter("lohi")
    precios = app.inventory.get_all_prices()

    for i in range(len(precios) - 1):
        actual = precios[i]
        siguiente = precios[i + 1]

        assert actual <= siguiente, f"Error: {actual} no es menor que {siguiente}"

def test_filter_hilo(app):
    app.inventory.apply_filter("hilo")
    precios = app.inventory.get_all_prices()

    for i in range(len(precios) - 1):
        actual = precios[i]
        siguiente = precios[i + 1]

        assert actual >= siguiente, f"Error: {actual} no es mayor que {siguiente}"


def test_filter_name_za(app):

    app.inventory.apply_filter("za")
    nombres_web = app.inventory.get_all_names()
    nombres_esperados = sorted(nombres_web, reverse=True)
    assert nombres_web == nombres_esperados, f"El orden Z-A falló. Web: {nombres_web}"

def test_filter_name_az(app):
    app.inventory.apply_filter("az")
    nombres_web = app.inventory.get_all_names()
    nombres_esperados = sorted(nombres_web, reverse=False)
    assert nombres_web == nombres_esperados, f"El orden Z-A falló. Web: {nombres_web}"
