class InventoryPage:
    def __init__(self, page):
        self.page = page

        self._add_backpack_btn = page.locator("#add-to-cart-sauce-labs-backpack")
        self._cart_badge = page.locator(".shopping_cart_badge")
        self._cart_check = page.locator(".shopping_cart_link")

        self._filter_dropdown = page.locator(".product_sort_container")
        self._product_names = page.locator(".inventory_item_name")
        self._product_prices = page.locator(".inventory_item_price")

        self._filter_dropdown = page.locator('select[data-test="product-sort-container"]')
        self._item_prices = page.locator('.inventory_item_price')


    def navigation(self):
        self.page.goto("https://www.saucedemo.com/inventory.html")
    def add_backpack_to_cart(self): #Funcion para añadir elemento al carrito
        self._add_backpack_btn.click()

    def remove_backpack_to_cart(self): #Funcion para quitar elemento del carrito
        self._cart_badge.click()

    def get_cart_count(self):
        return self._cart_badge.text_content()

    def check_cart(self):
        self._cart_check.click()

    def apply_filter(self, sort_value):
        """Aplica el filtro según el value: 'az', 'za', 'lohi', 'hilo'"""
        self._filter_dropdown.select_option(sort_value)

    def get_all_prices(self):
        """Captura todos los precios y los convierte a una lista de números (floats)"""
        prices_text = self._item_prices.all_text_contents()
        # Limpiamos el "$" y convertimos a número: ["$9.99"] -> [9.99]
        return [float(p.replace('$', '')) for p in prices_text]

    def get_all_names(self):
        """Captura todos los nombres de los productos y los devuelve en una lista"""
        return self.page.locator(".inventory_item_name").all_text_contents()
