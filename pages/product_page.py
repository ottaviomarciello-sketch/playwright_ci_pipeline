import re
from playwright.sync_api import Page, expect


class ProductPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.title = page.locator("#productTitle")
        self.cart = page.locator("#nav-cart-count")

        self.email_textbox = page.get_by_role(
            "textbox",
            name="Inserisci il numero di"
        )

        self.add_to_cart_button = page.locator(
            "#buybox input#add-to-cart-button"
        )

        self.add_protection_button = page.get_by_role(
            "button",
            name="Aggiungi protezione",
            exact=True
        )

        self.continue_button = page.get_by_role(
            "button",
            name="Continua"
        )

        self.proceed_to_order_button = page.get_by_role(
            "button",
            name=re.compile(r"^Procedi all'ordine.*")
        )

        self.checkbox = page.locator(
            ".a-row.a-spacing-top-small > .a-checkbox > label > .a-icon"
        ).first

    def get_title(self) -> str:
        expect(self.title).to_be_visible(timeout=10000)
        return self.title.inner_text().strip()

    def get_price(self) -> str:
        selectors = [
            ".a-price .a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice"
        ]

        for selector in selectors:
            locator = self.page.locator(selector).first

            try:
                expect(locator).to_be_visible(timeout=2000)
                return locator.inner_text().strip()
            except Exception:
                pass

        return "Prezzo non disponibile"

    def add_to_cart(self):
        expect(self.add_to_cart_button).to_be_visible(timeout=10000)
        self.add_to_cart_button.click()

    def proceed_to_order(self):
        expect(self.proceed_to_order_button).to_be_visible(timeout=10000)
        self.proceed_to_order_button.click()

    def enter_email(self, email: str):
        expect(self.email_textbox).to_be_visible(timeout=10000)
        self.email_textbox.fill(email)

    def click_checkbox(self):
        if self.checkbox.count() > 0:
            self.checkbox.click()
        else:
            print("Checkbox non presente.")

    def add_protection(self):
        if self.add_protection_button.count() > 0:
            self.add_protection_button.click()
        else:
            print("protezione acquisti non trovata")

    def get_cart_count(self) -> int:
        expect(self.cart).to_be_visible(timeout=10000)
        return int(self.cart.inner_text())

    def click_continue(self):
        self.continue_button.click()

    def take_screenshot(self):
        self.page.screenshot(
            path="screenshots/product.png",
            full_page=True
        )