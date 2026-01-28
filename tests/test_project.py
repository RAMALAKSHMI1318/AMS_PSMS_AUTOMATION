# from playwright.sync_api import Page
# from pages.login_page import LoginPage
# from pages.project_page import ProjectPage
# from utils.allure_helper import AllureHelper
# import pandas as pd


# TEST_DATA_PATH = "data/testdata.xlsx"
# PROJECT_SHEET = "project"

# test_data_df = pd.read_excel(TEST_DATA_PATH, sheet_name=PROJECT_SHEET)


# def test_prj_01_add_project(page: Page):
#     tcid = "PRJ_01"
#     AllureHelper.attach_common_description(tcid)

#     # ---------- Read row ----------
#     row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")[0]

#     # ---------- Parse Test Data ----------
#     data_map = {}
#     for item in row["Test Data"].split(","):
#         if ":" in item:
#             key, val = item.split(":", 1)
#             data_map[key.strip().lower()] = val.strip()

#     email = data_map["email"]
#     password = data_map["password"]

#     po_no = data_map["po_no"]
#     project_name = data_map["project_name"]
#     customer = data_map["customer"]
#     description = data_map["desc"]
#     qty = data_map["qty"]
#     remark = data_map["remark"]

#     expected_result = row.get("Expected Result", "")

#     login_page = LoginPage(page)
#     project_page = ProjectPage(page)

#     try:
#         login_page.open_login()
#         login_page.login(email, password)

#         project_page.open_add_project()
#         project_page.fill_project_details(
#             po_no=po_no,
#             project_name=project_name,
#             customer=customer,
#             description=description,
#             qty=qty,
#             remark=remark,
#         )

#         project_page.select_pdc_date("26")
#         project_page.save_project()

#         project_page.verify_project_created(project_name)

#         AllureHelper.attach_pass_description(tcid)
        

#     except Exception as e:
#         AllureHelper.attach_fail_description(tcid)
#         AllureHelper.attach_failure(str(e))
#         raise


import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from utils.allure_helper import AllureHelper
import pandas as pd


# ===============================
# TEST DATA CONFIG
# ===============================
TEST_DATA_PATH = "data/testdata.xlsx"
PROJECT_SHEET = "project"

test_data_df = pd.read_excel(TEST_DATA_PATH, sheet_name=PROJECT_SHEET)


# ===============================
# COMMON DATA PARSER (SAFE)
# ===============================
def get_test_data(tcid: str):
    row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")[0]

    data_map = {}
    test_data = row.get("Test Data")

    # ✅ Handle NaN / empty Test Data (PRJ_03 case)
    if not isinstance(test_data, str):
        return data_map

    for item in test_data.split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    return data_map


# =====================================================
# PRJ_01 – ADD PROJECT
# =====================================================
@pytest.mark.add
def test_prj_01_add_project(page: Page):
    tcid = "PRJ_01"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    try:
        login_page.open_login()
        login_page.login(data["email"], data["password"])

        project_page.open_add_project()

        project_page.fill_basic_details(
            po_no=data["po_no"],
            project_name=data["project_name"],
            customer_name=data["customer"],
        )

        project_page.select_pdc_date(data.get("pdc_day", "26"))

        if data.get("engineer"):
            project_page.select_responsible_engineer(data["engineer"])

        project_page.add_first_product(
            product_id=data["product1_id"],
            description=data["product1_desc"],
            qty=data["product1_qty"],
        )

        if data.get("product2_id"):
            project_page.add_second_product(
                product_id=data["product2_id"],
                product_name=data["product2_name"],
                description=data["product2_desc"],
                qty=data["product2_qty"],
            )

        project_page.add_remark(data["remark"])
        project_page.save_project()

        project_page.verify_project_created(data["project_name"])
        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise


# =====================================================
# PRJ_02 – EDIT PROJECT
# =====================================================
@pytest.mark.edit
def test_prj_02_edit_project(page: Page):
    tcid = "PRJ_02"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    try:
        login_page.open_login()
        login_page.login(data["email"], data["password"])

        page.get_by_role("link", name="Projects").click()
        project_page.open_edit_project()

        if data.get("pdc_day"):
            project_page.update_pdc_date(data["pdc_day"])

        if data.get("customer"):
            project_page.update_customer_name(data["customer"])

        if data.get("remark"):
            project_page.update_remark(data["remark"])

        project_page.update_project()
        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise


# =====================================================
# PRJ_03 – TREE EXPANSION (EXCEL DRIVEN)
# =====================================================
@pytest.mark.tree
def test_prj_03_project_tree_expansion(page: Page):
    tcid = "PRJ_03"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    try:
        # ✅ Safe login fallback
        email = data.get("email", "E04")
        password = data.get("password", "superadmin")

        login_page.open_login()
        login_page.login(email, password)

        page.get_by_role("link", name="Projects").click()

        project_page.open_project_tree()

        # ---------- TREE PATH FROM EXCEL ----------
        tree_path = data.get("tree_path")
        assert tree_path, "tree_path not provided in Excel for PRJ_03"

        nodes = [n.strip() for n in tree_path.split(">")]

        project_page.expand_tree_using_exact_locators(nodes)
        project_page.verify_tree_expanded()

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise
