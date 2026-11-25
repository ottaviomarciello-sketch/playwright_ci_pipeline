import re

from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_count = page.locator("#nav-cart-count")
        self.cart_link = page.locator("#nav-cart")
        self.active_items = page.locator("#sc-active-cart .sc-list-item")
        self.proceed_to_order_button = page.get_by_role(
            "button", name=re.compile(r"^Procedi all'ordine")
        )

    def open(self):
        self.cart_link.click(timeout=15000)

    def item_by_name(self, name: str) -> Locator:
        return self.active_items.filter(
            has=self.page.get_by_text(name, exact=True)
        )

    def proceed_to_order(self):
        self.proceed_to_order_button.click(timeout=10000)