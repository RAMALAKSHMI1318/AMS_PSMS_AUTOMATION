import re
import pytest
import pandas as pd
import time
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.excel_helper import update_excel_status
from utils.allure_helper import AllureHelper


TEST_DATA_FILE = "data/testdata.xlsx"


def get_test_data(tcid: str):
    df = pd.read_excel(TEST_DATA_FILE)
    row = df[df["TC ID"] == tcid].iloc[0]

    test_data = str(row["Test Data"])
    email = re.search(r"Email:\s*([^\s]+)", test_data).group(1)
    password = re.search(r"Password:\s*([^\s]+)", test_data).group(1)

    return {
        "email": email,
        "password": password,
        "expected": row["Expected Result"]
    }


def test_tc_login_01_valid_login(page: Page):
    tcid = "TC_LOGIN_01"
    data = get_test_data(tcid)

    AllureHelper.attach_description(tcid)
    login_page = LoginPage(page)

    try:
      
        login_page.open_login_page()
        login_page.login(data["email"], data["password"])
        login_page.assert_login_success()
        time.sleep(1)
        page.close()
        update_excel_status(
            TEST_DATA_FILE,
            tcid,
            status="Passed",
            remarks=data["expected"]
        )

        AllureHelper.attach_text(
            "Result",
            "Login successful, browser closed after 1 minute"
        )

    except Exception as e:
        screenshot_path = login_page.take_screenshot(tcid)

        update_excel_status(
            TEST_DATA_FILE,
            tcid,
            status="Failed",
            remarks=str(e)
        )

        AllureHelper.attach_text("Error", str(e))
        AllureHelper.attach_screenshot(screenshot_path)

        pytest.fail(f"{tcid} Failed: {str(e)}")
