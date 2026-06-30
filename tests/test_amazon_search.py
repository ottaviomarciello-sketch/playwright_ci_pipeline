from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.csv_writer import save_product


def test_amazon_search():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        page.keyboard.press("F11")

        # Home Page
        home = HomePage(page)
        home.open()
        home.search_product("monitor 27 pollici")

        # Search Results
        results = SearchResultsPage(page)

        results.verify_results_loaded()

        count = results.count_results()
        print(f"\nRisultati trovati: {count}")

        results.open_first_product()

        # Product Page
        product = ProductPage(page)

        title = product.get_title()
        price = product.get_price()

        print(f"\nTitolo: {title}")
        print(f"Prezzo: {price}")

        product.take_screenshot()
        #print(page.locator("#add-to-cart-button").count())
        #page.pause()
        # Aggiunge il prodotto al carrello
        product.add_to_cart()

        # Seleziona la protezione
        product.click_checkbox()
        product.add_protection()

        page.wait_for_timeout(5000)

        # Verifica il numero di articoli nel carrello
        assert product.get_cart_count() == 2

        # Procede all'ordine
        product.proceed_to_order()

        product.enter_email("ottaviomarciello@gmail.com")

        # Salva i dati del prodotto
        save_product(title, price)

        # Pausa per debug (rimuovere nei test automatici)
        page.pause()

        browser.close()




