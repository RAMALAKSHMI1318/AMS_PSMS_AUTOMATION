import time
import pytest
import pandas as pd
import re
import os
from pages.login_page import LoginPage
from playwright.sync_api import Page, expect
from utils.allure_helper import AllureHelper

# 🔹 Excel test data file
TEST_DATA_FILE = "data/testdata.xlsx"

# 🔹 Load Excel once
test_data_df = pd.read_excel(TEST_DATA_FILE)


def update_excel_and_report(page_obj, tcid, expected, passed, error=""):
    """
    Helper to update Excel status and take screenshot on failure
    (same logic as previous project, CSV -> XLSX)
    """
    index = test_data_df[test_data_df["TC ID"] == tcid].index[0]

    if passed:
        test_data_df.at[index, "Status"] = "Passed"
        test_data_df.at[index, "Remarks"] = expected
    else:
        test_data_df.at[index, "Status"] = "Failed"
        test_data_df.at[index, "Remarks"] = f"Expected: {expected} | Actual: {error}"

        if not os.path.exists("reports"):
            os.makedirs("reports")

        screenshot_path = os.path.join("reports", f"{tcid}_failure.png")
        page_obj.take_screenshot(screenshot_path)

    test_data_df.to_excel(TEST_DATA_FILE, index=False)


# ======================================================================
# TC_LOGIN_01 – Valid email & valid password
# ======================================================================
def test_tc_login_01_valid_login(page: Page):
    tcid = "TC_LOGIN_01"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\n\r]*)", test_data_str)
    password_match = re.search(r"Password:\s*([^\n\r]*)", test_data_str)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        # ✅ Success = no error message
        expect(login_page.error_message).not_to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_02 – Valid email & invalid password
# ======================================================================
def test_tc_login_02_invalid_password(page: Page):
    tcid = "TC_LOGIN_02"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\n\r]*)", test_data_str)
    password_match = re.search(r"Password:\s*([^\n\r]*)", test_data_str)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_03 – Invalid email & valid password
# ======================================================================
def test_tc_login_03_invalid_email(page: Page):
    tcid = "TC_LOGIN_03"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\n\r]*)", test_data_str)
    password_match = re.search(r"Password:\s*([^\n\r]*)", test_data_str)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_04 – Invalid email & invalid password
# ======================================================================
def test_tc_login_04_invalid_email_invalid_password(page: Page):
    tcid = "TC_LOGIN_04"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\n\r]*)", test_data_str)
    password_match = re.search(r"Password:\s*([^\n\r]*)", test_data_str)

    email = email_match.group(1).strip() if email_match else ""
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_05 – Empty email & empty password
# ======================================================================
def test_tc_login_05_empty_email_empty_password(page: Page):
    tcid = "TC_LOGIN_05"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login("", "")

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_06 – Empty email
# ======================================================================
def test_tc_login_06_empty_email(page: Page):
    tcid = "TC_LOGIN_06"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    password_match = re.search(r"Password:\s*([^\n\r]*)", test_data_str)
    password = password_match.group(1).strip() if password_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login("", password)

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")


# ======================================================================
# TC_LOGIN_07 – Empty password
# ======================================================================
def test_tc_login_07_empty_password(page: Page):
    tcid = "TC_LOGIN_07"
    AllureHelper.attach_description(tcid)

    tc_row = test_data_df[test_data_df["TC ID"] == tcid].iloc[0]
    expected = tc_row["Expected Result"]

    test_data_str = str(tc_row.get("Test Data", ""))
    email_match = re.search(r"Email:\s*([^\n\r]*)", test_data_str)
    email = email_match.group(1).strip() if email_match else ""

    login_page = LoginPage(page)

    try:
        login_page.open_login()
        login_page.login(email, "")

        expect(login_page.error_message).to_be_visible(timeout=5000)

        time.sleep(1)
        page.close()

        update_excel_and_report(login_page, tcid, expected, passed=True)

    except Exception as e:
        update_excel_and_report(login_page, tcid, expected, passed=False, error=str(e))
        pytest.fail(f"{tcid} Failed: {str(e)}")
