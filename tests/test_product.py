from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.Product_page import ProductPage
from utils.allure_helper import AllureHelper
import pandas as pd
import time   # ✅ add this


TEST_DATA_PATH = "data/testdata.xlsx"
PRODUCT_SHEET = "Product"

test_data_df = pd.read_excel(TEST_DATA_PATH, sheet_name=PRODUCT_SHEET)


def test_prd_01_add_product(page: Page):
    tcid = "PRD_01"
    AllureHelper.attach_common_description(tcid)

    # ===============================
    # READ TEST DATA ROW
    # ===============================
    row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")[0]

    # ===============================
    # PARSE TEST DATA
    # ===============================
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map["email"]
    password = data_map["password"]

    product_name = data_map["product_name"]
    category = data_map["category"]
    status = data_map["status"]
    description = data_map["description"]

    # ✅ DYNAMIC PRODUCT CODE (NEW)
    product_code = f"PRD{int(time.time() % 100000)}"

    # ===============================
    # PAGE OBJECTS
    # ===============================
    login_page = LoginPage(page)
    product_page = ProductPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        product_page.open_product_screen()

        product_page.enter_product_details(
            code=product_code,
            name=product_name,
            category=category,
            status=status,
            description=description
        )

        product_page.save()

        product_page.verify_product_created(product_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise
