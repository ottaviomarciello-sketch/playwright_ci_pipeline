from playwright.sync_api import Page


class HomePage:
    # Classe che rappresenta la Home Page di Amazon (Page Object Model)

    def __init__(self, page: Page):
        # Costruttore: viene chiamato quando crei HomePage(page)
        self.page = page  # pagina Playwright (tab del browser)

        self.url = "https://www.amazon.it"  # URL della home page Amazon

        # Selettore CSS del bottone cookie "Accetta"
        self.cookie_button = "#sp-cc-accept"

        # Selettore della barra di ricerca
        self.search_input = "#twotabsearchtextbox"

        # Selettore del bottone di ricerca (lente)
        self.search_button = "#nav-search-submit-button"

    def open(self):
        # Metodo per aprire la home page di Amazon

        self.page.goto(
            self.url,  # apre l'URL definito sopra
            wait_until="domcontentloaded",  # aspetta che il DOM (HTML) sia caricato
            timeout=60000  # timeout massimo 60 secondi
        )

        # ulteriore attesa per sicurezza (pagina stabile)
        self.page.wait_for_load_state("domcontentloaded")

        # prova ad accettare i cookie (se popup presente)
        self.accept_cookies()

    def accept_cookies(self):
        # Metodo per chiudere il popup cookie se appare

        try:
            # cerca il bottone cookie e clicca
            self.page.locator(self.cookie_button).click(timeout=3000)
        except:
            # se il bottone non esiste o non appare entro 3 secondi
            # non bloccare il test
            pass

    def search_product(self, text: str):
        # Metodo per cercare un prodotto su Amazon

        # scrive il testo nella barra di ricerca
        self.page.locator(self.search_input).fill(text)

        # clicca il bottone di ricerca
        self.page.locator(self.search_button).click()