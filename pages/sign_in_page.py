from playwright.sync_api import Page


class SignInPage:
    def __init__(self, page: Page):
        self.email = page.locator("#ap_email, #ap_email_login")
        self.password = page.locator("#ap_password")
        self.continue_button = page.get_by_role(
            "button", name="Continua", exact=True
        )
        self.sign_in_button = page.get_by_role(
            "button", name="Accedi", exact=True
        )

    def sign_in(self, email: str, password: str):
        self.email.fill(email)
        self.continue_button.click()
        self.password.fill(password)
        self.sign_in_button.click()