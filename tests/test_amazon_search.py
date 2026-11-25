import re
from urllib.parse import urlsplit

from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


def test_search_opens_first_product(page):
    home = HomePage(page)
    home.open()
    home.search_product("monitor 27 pollici")

    results = SearchResultsPage(page)
    product_path = urlsplit(results.first_product_url()).path

    asin_match = re.search(
        r"/dp/([A-Z0-9]{10})(?:/|$)", product_path, re.IGNORECASE
    )
    assert asin_match, f"ASIN non trovato nel link del prodotto: {product_path}"
    asin = asin_match.group(1)

    product = results.open_first_product()

    expected_url = re.compile(
        rf"/(?:dp|gp/product)/{re.escape(asin)}(?:[/?#]|$)",
        re.IGNORECASE,
    )
    expect(page).to_have_url(expected_url, timeout=15000)
    assert product.get_title(), "Il titolo del prodotto è vuoto"