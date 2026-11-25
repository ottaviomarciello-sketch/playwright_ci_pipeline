from playwright.sync_api import Page, expect

from pages.product_page import ProductPage


class SearchResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.results = page.locator('[data-component-type="s-search-result"]')
        self.first_product_link = (
            self.results.locator('a[href*="/dp/"]')
            .filter(has=page.locator("h2"))
            .first
        )

    def verify_results_loaded(self):
        expect(self.first_product_link).to_be_visible(timeout=15000)

    def count_results(self) -> int:
        self.verify_results_loaded()
        return self.results.count()

    def first_product_url(self) -> str:
        self.verify_results_loaded()
        return self.first_product_link.evaluate("(link) => link.href")

    def open_first_product(self) -> ProductPage:
        self.first_product_link.click(timeout=15000)
        return ProductPage(self.page)