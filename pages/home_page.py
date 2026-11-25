from playwright.sync_api import Page, TimeoutError


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.amazon.it"
        self.cookie_button = page.locator("#sp-cc-accept")
        self.search_input = page.locator("#twotabsearchtextbox")
        self.search_button = page.locator("#nav-search-submit-button")

    def open(self):
        self.page.goto(
            self.url,
            wait_until="domcontentloaded",
            timeout=60000,
        )
        self.accept_cookies()

    def accept_cookies(self):
        try:
            self.cookie_button.wait_for(state="visible", timeout=3000)
        except TimeoutError:
            return

        self.cookie_button.click(timeout=3000)

    def search_product(self, text: str):
        self.search_input.fill(text)
        self.search_button.click()