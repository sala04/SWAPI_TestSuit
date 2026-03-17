from playwright.sync_api import Page


class SauceDemoInventoryPage:

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        #cart
        self.shopping_cart_link = page.locator('data-test=shopping-cart-link')
        self.cart_badge = page.locator('data-test=shopping-cart-badge')

        #left menu
        self.open_menu_button = page.locator('id=react-burger-menu-btn')
        self.close_menu_button = page.locator('id=react-burger-cross-btn')
        self.logout_sidebar_link = page.locator('data-test=logout-sidebar-link')
        self.reset_sidebar_link = page.locator('data-test=reset-sidebar-link')
        self.about_sidebar_link = page.locator('data-test=about-sidebar-link')
        self.all_items_sidebar_link = page.locator('data-test=inventory-sidebar-link')

        #sort
        self.product_sort_container = page.locator('data-test=product-sort-container')
        self.active_option = page.locator('data-test=active-option')

        #inventory
        self.inventory_container = page.locator('data-test=inventory-container')
        self.inventory_items = page.locator('data-test=inventory-item')
        self.inventory_item_names = page.locator('data-test=inventory-item-name')
        self.inventory_item_prices = page.locator('data-test=inventory-item-price')


    def load(self) -> None:
        self.page.goto(self.URL)

    def open_menu(self) -> None:
        self.open_menu_button.click()

    def close_menu(self) -> None:
        self.close_menu_button.click()

    def logout(self) -> None:
        self.open_menu()
        self.logout_sidebar_link.click()

    def sort_by(self, value: str) -> None:
        """
        Values:
        - 'az'
        - 'za'
        - 'lohi'
        - 'hilo'
        """
        allowed_values = {'az', 'za', 'lohi', 'hilo'}
        assert value in allowed_values, f"Wrong sorting input. Allowed values are {allowed_values}"
        self.product_sort_container.select_option(value)

    def get_inventory_count(self) -> int:
        return self.inventory_items.count()

    def get_product_names(self) -> list:
        return self.inventory_item_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices = self.inventory_item_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in prices] #return as float so they can be properly sorted

    def get_all_product_image_sources(self) -> list[str]:
        srcs = []
        for i in range(self.inventory_items.count()):
            item = self.inventory_items.nth(i)
            img = item.locator("img")
            src = img.get_attribute("src")
            srcs.append(src)

        return srcs

    def get_cart_badge_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content())

    def click_product_to_cart_by_name(self, product_name: str) -> None:
        item = self.inventory_items.filter(
            has=self.page.locator('data-test=inventory-item-name', has_text=product_name)
        )
        item.locator("button").click()

    def is_add_button_visible(self, product_name: str) -> bool:
        item = self.inventory_items.filter(has_text=product_name)
        return item.get_by_role("button", name="Add to cart").is_visible()

    def is_remove_button_visible(self, product_name: str) -> bool:
        item = self.inventory_items.filter(has_text=product_name)
        return item.get_by_role("button", name="Remove").is_visible()

    def click_detail_view(self, product_name: str) -> None:
        item = self.inventory_items.filter(has_text=product_name)
        item.locator('data-test=inventory-item-name').click()

    def go_to_cart(self) -> None:
        self.shopping_cart_link.click()