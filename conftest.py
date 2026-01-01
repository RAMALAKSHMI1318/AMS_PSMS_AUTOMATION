import pytest
import allure
from config import ARTIFACTS_DIR
import os
import time


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure and attach to Allure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            # Create artifacts directory if not exists
            os.makedirs(ARTIFACTS_DIR, exist_ok=True)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(ARTIFACTS_DIR, screenshot_name)

            # Take screenshot
            page.screenshot(path=screenshot_path)

            # Attach to Allure
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )

            print(f"\n📸 Screenshot saved & attached to Allure: {screenshot_path}")
