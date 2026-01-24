import random
import pandas as pd
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.users_page import UserPage
from utils.allure_helper import AllureHelper


TEST_DATA_PATH = "data/testdata.xlsx"
test_data_df = pd.read_excel(TEST_DATA_PATH)


def test_usr_01_add_user(page: Page):

    tcid = "USR_01"
    AllureHelper.attach_common_description(tcid)

    # ---------- Read Excel ----------
    row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")[0]

    data_map = {}
    for item in str(row["Test Data"]).replace("\n", ",").split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    full_name = data_map.get("fullname")
    designation = data_map.get("designation")
    department = data_map.get("department")
    role = data_map.get("role")
    position = data_map.get("position")
    user_email = data_map.get("useremail")

    # ---------- Dynamic values (SAME AS MACHINES) ----------
    employee_code = f"EMP{random.randint(10000, 99999)}"
    office_number = str(random.randint(10000000000, 99999999999))
    mobile_number = str(random.randint(7000000000, 9999999999))

    login_page = LoginPage(page)
    user_page = UserPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        user_page.open_user_page()

        user_page.fill_user_details(
            employee_code=employee_code,
            full_name=full_name,
            designation=designation,
            office_number=office_number,
            mobile_number=mobile_number,
            email=user_email,
            department=department,
            roles=role,
            position=position,
        )

        user_page.save()
        user_page.verify_user_created(full_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise
