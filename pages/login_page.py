from playwright.sync_api import Page, expect
from base.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 🔹 New project locators
        self.input_email = page.get_by_role("textbox", name="Email")
        self.input_password = page.get_by_role("textbox", name="Password")
        self.btn_login = page.get_by_role("button", name="Login")

        # 🔹 Error / validation message
        self.error_message = page.locator(
            ".error, .error-message, .alert-danger, .validation-error"
        )

    def open_login(self):
        self.navigate("login")

    def login(self, email: str, password: str):
        self.input_email.fill("")
        self.input_password.fill("")

        if email:
            self.input_email.fill(email)
        if password:
            self.input_password.fill(password)

        self.btn_login.click()
