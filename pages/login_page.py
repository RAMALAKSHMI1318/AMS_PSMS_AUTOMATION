from playwright.sync_api import Page, expect
from base.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")

        # Adjust selector if your app uses different error UI
        self.login_error = page.locator(".error, .error-message, .alert-danger")

    def open_login_page(self):
        self.navigate("login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def assert_login_success(self):
        """
        Success assertion WITHOUT waiting for redirect:
        Login is successful if no error message is shown
        """
        expect(self.login_error).not_to_be_visible(timeout=500)
