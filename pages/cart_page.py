class CartPage:
    def __init__(self, page): #Identificamos los parametros de la pagina
        self.page = page

        self._remove_btn = page.locator("#remove-sauce-labs-backpack")
        self._checkout_btn = page.locator("#checkout")
        self._continue_shopping = page.locator("#continue-shopping")
        self._cart_badge = page.locator(".shopping_cart_badge")
        self._filter = page.locator("product_sort_container")

    def navigation(self):
        self.page.goto("https://www.saucedemo.com/cart.html")
    def remove_item(self):
        self._remove_btn.click()

    def empty_cart_count(self):
        return not self._cart_badge.is_visible()

    def continue_shopping(self):
        self._continue_shopping.click()

    def check_out(self):
        self._checkout_btn.click()

