import re
from urllib.parse import urlsplit

from playwright.sync_api import TimeoutError, expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


def test_cart_contains_first_search_result(page):
    home = HomePage(page)
    home.open()
    home.search_product("monitor 27 pollici")

    results = SearchResultsPage(page)
    results.verify_results_loaded()
    product = results.open_first_product()

    product_title = product.get_title()
    assert product_title, "Il titolo del prodotto è vuoto"

    product_path = urlsplit(page.url).path
    asin_match = re.search(
        r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:/|$)",
        product_path,
        re.IGNORECASE,
    )
    assert asin_match, f"ASIN non trovato nell'URL del prodotto: {product_path}"
    product_asin = asin_match.group(1).upper()

    product.add_to_cart()

    expected_count = "1"
    try:
        product.add_protection_button.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        pass
    else:
        page.pause()
        product.select_protection_plan()
        product.add_protection()
        expected_count = "2"

    cart = CartPage(page)
    expect(cart.item_count).to_have_text(expected_count, timeout=15000)

    cart.open()
    cart_item = page.locator(
        f'#sc-active-cart [data-asin="{product_asin}"]'
    )
    expect(cart_item).to_be_visible(timeout=15000)