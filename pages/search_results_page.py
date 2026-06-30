from playwright.sync_api import Page, expect
from pages.product_page import ProductPage


class SearchResultsPage:
    """Page Object della pagina risultati Amazon"""

    def __init__(self, page: Page):
        self.page = page

        # Locator
        self.results = '[data-component-type="s-search-result"]'
        self.cookie_button = "#sp-cc-accept"
        self.product_links = (
            '[data-component-type="s-search-result"] h2'
        )

    def accept_cookies(self):
        """Accetta i cookie se il popup è presente"""

        try:
            self.page.locator(self.cookie_button).click(timeout=3000)
        except Exception:
            pass

    def verify_results_loaded(self):
        """Verifica che almeno un risultato sia visibile"""

        self.accept_cookies()

        expect(
            self.page.locator(self.results).first
        ).to_be_visible(timeout=15000)

    def count_results(self):
        """Restituisce il numero di risultati presenti"""

        self.accept_cookies()

        expect(
            self.page.locator(self.results).first
        ).to_be_visible(timeout=15000)

        return self.page.locator(self.results).count()

    def open_first_product(self):
        """Apre il primo prodotto disponibile"""

        self.accept_cookies()

        expect(
            self.page.locator(self.results).first
        ).to_be_visible(timeout=15000)

        links = self.page.locator(self.product_links)
        #self.page.pause()
        count = links.count()

        if count == 0:
            self.page.screenshot(
                path="screenshots/no_products_found.png",
                full_page=True
            )
            raise Exception("Nessun prodotto trovato")

        for i in range(count):

            link = links.nth(i)

            try:
                link.click(timeout=5000)

                expect(
                    self.page.locator("span#productTitle")
                ).to_be_visible(timeout=10000)

                return ProductPage(self.page)

            except Exception as e:
                print(f"Link {i} fallito: {e}")

        self.page.screenshot(
            path="screenshots/no_clickable_product.png",
            full_page=True
        )

        raise Exception("Nessun prodotto cliccabile trovato")