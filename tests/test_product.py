from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.Product_page import ProductPage
from utils.allure_helper import AllureHelper
from utils.excel_helper import update_excel_status
import pandas as pd
import time   # ✅ add this
import pytest


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
    category_index = int(data_map["category_index"])
    status_index = int(data_map["status_index"])
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

        product_page.enter_product_details (
            code=product_code,
            name=product_name,
            
            description=description
        )
        
        product_page.select_category_by_index(category_index)
        product_page.select_status_by_index(status_index)


        product_page.save()

        product_page.verify_product_created(product_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise


@pytest.mark.assign
def test_prd_02_assign_user(page: Page):
    tcid = "PRD_02"
    AllureHelper.attach_common_description(tcid)

    # READ TEST DATA ROW (safe)
    rows = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")
    data_map = {}
    if rows:
        row = rows[0]
        test_data = row.get("Test Data", "")
        if isinstance(test_data, str):
            for item in test_data.split(","):
                if ":" in item:
                    key, val = item.split(":", 1)
                    data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email", "E07")
    password = data_map.get("password", "superadmin")
    user = data_map.get("user", "jyothi")
    role = data_map.get("role", "Super Admin")

    login_page = LoginPage(page)
    product_page = ProductPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        product_page.open_product_screen()
        # open first product tree/icon using safe method that handles dialog masks
        product_page.open_product_tree()

        product_page.assign_user_by_names(user, role)
        product_page.verify_user_assigned(user)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise


@pytest.mark.milestone
def test_prd_03_add_milestone(page: Page):
    tcid = "PRD_03"
    AllureHelper.attach_common_description(tcid)

    # READ TEST DATA ROW (safe)
    rows = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")
    data_map = {}
    if rows:
        row = rows[0]
        test_data = row.get("Test Data", "")
        if isinstance(test_data, str):
            for item in test_data.split(","):
                if ":" in item:
                    key, val = item.split(":", 1)
                    data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email", "E07")
    password = data_map.get("password", "superadmin")

    milestone_name = data_map.get("milestone_name", "Design Phase")
    milestone_code = data_map.get("milestone_code", "MS-001")
    weightage = data_map.get("weightage", "20")
    remarks = data_map.get("remarks", "Initial design milestone")
    product_name = data_map.get("product_name", "")

    login_page = LoginPage(page)
    product_page = ProductPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        product_page.open_product_screen()
        # open the product tree and select the product if given
        product_page.open_product_tree(product_name if product_name else None)

        product_page.create_milestone(
            name=milestone_name,
            code=milestone_code,
            weightage=weightage,
            remarks=remarks,
        )

        product_page.verify_milestone_created(milestone_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise


@pytest.mark.assign
def test_prd_04_assign_user_on_milestone(page: Page):
    tcid = "PRD_04"
    AllureHelper.attach_common_description(tcid)

    rows = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")
    data_map = {}
    if rows:
        row = rows[0]
        test_data = row.get("Test Data", "")
        if isinstance(test_data, str):
            for item in test_data.split(","):
                if ":" in item:
                    key, val = item.split(":", 1)
                    data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email", "E07")
    password = data_map.get("password", "superadmin")
    product_name = data_map.get("product_name", "product2")
    milestone_name = data_map.get("milestone_name", "Design Phase")
    user = data_map.get("user", "jyothi")
    role = data_map.get("role", "Super Admin")

    user_index = None
    role_index = None
    if data_map.get("user_index") is not None and str(data_map.get("user_index")).strip() != "":
        user_index = int(data_map.get("user_index"))
    if data_map.get("role_index") is not None and str(data_map.get("role_index")).strip() != "":
        role_index = int(data_map.get("role_index"))

    login_page = LoginPage(page)
    product_page = ProductPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        product_page.open_product_screen()
        product_page.open_product_tree(product_name if product_name else None)

        # Select the milestone node (like clicking 'Design Phase')
        product_page.select_milestone_by_name(milestone_name)

        # Assign by name if provided, otherwise by index
        if user and role:
            product_page.assign_user_by_names(user, role)
        elif user_index is not None and role_index is not None:
            product_page.assign_user_to_product(user_index, role_index)
        else:
            raise ValueError("No user/role data provided for assignment")

        product_page.verify_user_assigned(user)

        # Update Excel status
        update_excel_status(TEST_DATA_PATH, tcid, "Pass", "User assigned successfully")

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        update_excel_status(TEST_DATA_PATH, tcid, "Fail", str(e))
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise