import pytest
import allure
from playwright.sync_api import sync_playwright


# =====================================================
# Playwright Page Fixture (REQUIRED)
# =====================================================
@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=500
        )
        context = browser.new_context()
        page = context.new_page()

        yield page

        context.close()
        browser.close()


# =====================================================
# Allure Screenshot on Failure (YOUR EXISTING CODE)
# =====================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot on test failure and attach to Allure
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
