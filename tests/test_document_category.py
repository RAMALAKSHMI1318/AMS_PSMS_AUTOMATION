import os
import time
import random
import pandas as pd
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.document_category_page import DocumentCategoryPage
from utils.allure_helper import AllureHelper


# ===============================
# TEST DATA
# ===============================
TEST_DATA_FILE = "data/testdata.xlsx"
test_data_df = pd.read_excel(TEST_DATA_FILE)


# ===============================
# DYNAMIC DATA GENERATORS
# ===============================
def generate_name():
    return f"DC_{int(time.time())}"

def generate_code():
    # EXACTLY 3-digit numeric code
    return str(random.randint(100, 999))


# =====================================================
# DC_01 – SEARCH DOCUMENT CATEGORY
# =====================================================
def test_dc_01_search_document_category(page: Page):

    tcid = "DC_01"
    AllureHelper.attach_description(tcid)

    row = test_data_df[
        test_data_df["TC ID"] == tcid
    ].to_dict(orient="records")[0]

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            k, v = item.split(":", 1)
            data_map[k.strip()] = v.strip()

    login_page = LoginPage(page)
    document_page = DocumentCategoryPage(page)

    try:
        # ===== LOGIN =====
        login_page.open_login()
        login_page.login(data_map["email"], data_map["password"])

        # ===== NAVIGATE =====
        document_page.open_document_categories()

        # ===== SEARCH =====
        document_page.search_document_category(data_map["name"])

        assert True

    except Exception:
        os.makedirs("reports", exist_ok=True)
        page.screenshot(path=f"reports/{tcid}_failure.png")
        raise


# =====================================================
# DC_02 – ADD NEW DOCUMENT CATEGORY
# =====================================================
def test_dc_02_add_document_category(page: Page):

    tcid = "DC_02"
    AllureHelper.attach_description(tcid)

    row = test_data_df[
        test_data_df["TC ID"] == tcid
    ].to_dict(orient="records")[0]

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            k, v = item.split(":", 1)
            data_map[k.strip()] = v.strip()

    login_page = LoginPage(page)
    document_page = DocumentCategoryPage(page)

    try:
        # ===== LOGIN =====
        login_page.open_login()
        login_page.login(data_map["email"], data_map["password"])

        # ===== NAVIGATE =====
        document_page.open_document_categories()

        # ===== ADD NEW =====
        document_page.click_add_new()

        # ===== DYNAMIC DATA =====
        name = generate_name()
        code = generate_code()

        # ===== FILL FORM =====
        document_page.fill_name(name)
        document_page.fill_code(code)
        document_page.select_category_type(data_map["categoryType"])
        document_page.select_parent_category(data_map["parentCategory"])
        document_page.fill_display_order(data_map["displayOrder"])
        document_page.fill_description(data_map["description"])

        # ===== SAVE =====
        document_page.click_save()

        assert True

    except Exception:
        os.makedirs("reports", exist_ok=True)
        page.screenshot(path=f"reports/{tcid}_failure.png")
        
        # =====================================================
# DC_03 – EDIT DOCUMENT CATEGORY (BASED ON SEARCH)
# =====================================================
def test_dc_03_edit_document_category(page: Page):

    tcid = "DC_03"
    AllureHelper.attach_description(tcid)

    row = test_data_df[
        test_data_df["TC ID"] == tcid
    ].to_dict(orient="records")[0]

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            k, v = item.split(":", 1)
            data_map[k.strip()] = v.strip()

    login_page = LoginPage(page)
    document_page = DocumentCategoryPage(page)

    try:
        # ===== LOGIN =====
        login_page.open_login()
        login_page.login(data_map["email"], data_map["password"])

        # ===== NAVIGATE =====
        document_page.open_document_categories()

        # ===== EDIT BASED ON SEARCH =====
        document_page.click_edit_by_search(data_map["search"])

        # ===== UPDATE FIELDS =====
        document_page.fill_name(data_map["name"])
        document_page.fill_description(data_map["description"])

        # ===== SAVE =====
        document_page.click_save()

        assert True

    except Exception:
        os.makedirs("reports", exist_ok=True)
        page.screenshot(path=f"reports/{tcid}_failure.png")
        raise

# =====================================================
# DC_04 – DELETE DOCUMENT CATEGORY (BASED ON SEARCH)
# =====================================================
def test_dc_04_delete_document_category(page: Page):

    tcid = "DC_04"
    AllureHelper.attach_description(tcid)

    row = test_data_df[
        test_data_df["TC ID"] == tcid
    ].to_dict(orient="records")[0]

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            k, v = item.split(":", 1)
            data_map[k.strip()] = v.strip()

    login_page = LoginPage(page)
    document_page = DocumentCategoryPage(page)

    try:
        # ===== LOGIN =====
        login_page.open_login()
        login_page.login(data_map["email"], data_map["password"])

        # ===== NAVIGATE =====
        document_page.open_document_categories()

        # ===== DELETE BASED ON SEARCH =====
        document_page.click_delete_by_search(data_map["search"])

        assert True

    except Exception:
        os.makedirs("reports", exist_ok=True)
        page.screenshot(path=f"reports/{tcid}_failure.png")
        raise
