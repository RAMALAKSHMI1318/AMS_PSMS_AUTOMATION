import random
import time
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.machines_page import MachinesPage
from utils.allure_helper import AllureHelper
import pandas as pd



TEST_DATA_PATH = "data/testdata.xlsx"

test_data_df = pd.read_excel(TEST_DATA_PATH)

def test_machine01_add_machine(page: Page, request):

    tcid = "TC_Machine1"
    AllureHelper.attach_common_description(tcid)

    # ---------- Fetch test data from Excel ----------
    row = test_data_df[test_data_df["TC ID"] == tcid].to_dict(orient="records")[0]
    expected = row.get("Expected", "Machine created successfully")

    # ---------- Parse Test Data ----------
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    machine_name = data_map.get("machine_name")
    location = data_map.get("location")
    status_index = int(data_map.get("status_index", 0))

    # ---------- Dynamic values ----------
    machine_code = f"MC{random.randint(100, 999)}"
    serial_number = f"SN{int(time.time()) % 100000}"
    capacity = str(random.randint(1, 10))

    login_page = LoginPage(page)
    machines_page = MachinesPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        machines_page.open_add_machine()

        machines_page.enter_machine_details(
            code=machine_code,
            name=machine_name,
            serial=serial_number,
            qty=capacity,
            location=location
        )

        machines_page.select_status_by_index(status_index)

        machines_page.save()

        machines_page.verify_machine_created(machine_name)

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_machine02_search_machine(page: Page):
    tcid = "TC_Machine2"
    AllureHelper.attach_common_description(tcid)
    row = AllureHelper.get_test_row(tcid)
    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    machine_name = data_map.get("machine_name")

    login_page = LoginPage(page)
    machines_page = MachinesPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)
        machines_page.open_machines_tab()
        machines_page.search_machine(machine_name)
        time.sleep(4)
        machines_page.verify_machine_search_result(machine_name)
        AllureHelper.attach_pass_description(tcid)
    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_machine03_update_machine(page: Page):
    tcid = "TC_Machine3"

    AllureHelper.attach_common_description(tcid)

    row = AllureHelper.get_test_row(tcid)

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    base_machine_code = data_map.get("machine_code")
    location = data_map.get("location")

    login_page = LoginPage(page)
    machines_page = MachinesPage(page)

    try:
      
        login_page.open_login()
        login_page.login(email, password)

        machines_page.open_machines_tab()

        machines_page.search_machine(base_machine_code)
        time.sleep(2)

        machines_page.click_edit_first_machine()
        updated_machine_code = f"{base_machine_code}1"

        machines_page.update_machine_code(updated_machine_code)
        machines_page.update_location(location)
        machines_page.save_updated_machine()
        # machines_page.verify_machine_updated(updated_machine_code)
        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_machine04_delete_machine(page: Page):
    """
    TC_Machine4: Delete the machine
    """

    tcid = "TC_Machine4"

    # ---------- Allure common description ----------
    AllureHelper.attach_common_description(tcid)

    # ---------- Read test data from Excel ----------
    row = AllureHelper.get_test_row(tcid)

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    search_text = data_map.get("search")

    login_page = LoginPage(page)
    machines_page = MachinesPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        machines_page.open_machines_tab()

        machines_page.search_machine(search_text)

        machines_page.delete_first_machine()

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        # ---------- FAIL description ----------
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise




