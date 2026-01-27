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


from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from utils.allure_helper import AllureHelper
import pandas as pd


TEST_DATA_PATH = "data/testdata.xlsx"
PROJECT_SHEET = "project"

test_data_df = pd.read_excel(TEST_DATA_PATH, sheet_name=PROJECT_SHEET)


def test_prj_01_add_project(page: Page):
    tcid = "PRJ_01"
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

    po_no = data_map["po_no"]
    project_name = data_map["project_name"]
    customer_name = data_map["customer"]

    pdc_day = data_map.get("pdc_day", "26")
    engineer = data_map.get("engineer")

    product1_id = data_map["product1_id"]
    product1_desc = data_map["product1_desc"]
    product1_qty = data_map["product1_qty"]

    product2_id = data_map.get("product2_id")
    product2_name = data_map.get("product2_name")
    product2_desc = data_map.get("product2_desc")
    product2_qty = data_map.get("product2_qty")

    remark = data_map["remark"]

    # ===============================
    # PAGE OBJECTS
    # ===============================
    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    try:
        # ===============================
        # LOGIN
        # ===============================
        login_page.open_login()
        login_page.login(email, password)

        # ===============================
        # CREATE PROJECT
        # ===============================
        project_page.open_add_project()

        project_page.fill_basic_details(
            po_no=po_no,
            project_name=project_name,
            customer_name=customer_name,
        )

        project_page.select_pdc_date(pdc_day)

        if engineer:
            project_page.select_responsible_engineer(engineer)

        project_page.add_first_product(
            product_id=product1_id,
            description=product1_desc,
            qty=product1_qty,
        )

        if product2_id:
            project_page.add_second_product(
                product_id=product2_id,
                product_name=product2_name,
                description=product2_desc,
                qty=product2_qty,
            )

        project_page.add_remark(remark)
        project_page.save_project()

        # ===============================
        # VERIFICATION
        # ===============================
        project_page.verify_project_created(project_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise
