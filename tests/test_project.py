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

    # ---------- LOGIN ----------
    login_page.open_login()
    login_page.login(data["email"], data["password"])

    # ---------- OPEN ADD PROJECT ----------
    project_page.open_add_project()

    # ---------- BASIC DETAILS ----------
    project_page.fill_basic_details(
        po_no=data["po_no"],
        project_name=data["project_name"],
        customer_name=data["customer"],
    )

    # ---------- PDC DATE ----------
    project_page.select_pdc_date(data.get("pdc_day", "3"))

    # ---------- RESPONSIBLE ENGINEER ----------
    if data.get("engineer"):
        project_page.select_responsible_engineer(data["engineer"])

    # ---------- FIRST PRODUCT ----------
    project_page.add_first_product(
        product_id=data["product1_id"],
        description=data["product1_desc"],
        qty=data["product1_qty"],
    )

    # ---------- SECOND PRODUCT (OPTIONAL) ----------
    if data.get("product2_id"):
        project_page.add_second_product(
            product_id=data["product2_id"],
            product_name=data["product2_name"],
            description=data["product2_desc"],
            qty=data["product2_qty"],
        )

    # ---------- REMARK ----------
    project_page.add_remark(data["remark"])

    # ---------- SAVE ----------
    project_page.save_project()

    # ⛔ STOP HERE (AS REQUESTED)
    AllureHelper.attach_pass_description(tcid)


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


@pytest.mark.product
def test_prj_04_add_product_from_tree(page: Page):
    tcid = "PRJ_04"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    login_page.open_login()
    login_page.login(data["email"], data["password"])

    page.get_by_role("link", name="Projects").click()
    project_page.open_project_tree()

    # Right-click Project node
    project_page.right_click_on_project_node(data["project_name"])

    # Click + Product from context menu
    project_page.click_add_product_from_context()

    # Fill product form
    project_page.fill_product_details(
        product_name=data["product"],
        delivery_day=data["delivery_day"],
        quantity=data["quantity"],
        unit=data["unit"],
        remarks=data["remarks"],
        file_path=data["file_path"]
    )

    project_page.save_product()

    # ✅ PASS — creation itself is the validation
    AllureHelper.attach_pass_description(tcid)


@pytest.mark.milestone
def test_prj_05_add_milestone_from_tree(page: Page):
    tcid = "PRJ_05"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    # ---------- LOGIN ----------
    login_page.open_login()
    login_page.login(data["email"], data["password"])

    # ---------- NAVIGATE ----------
    page.get_by_role("link", name="Projects").click()

    # ---------- TREE FLOW (EXACT CODEGEN) ----------
    project_page.open_project_tree()
    project_page.expand_strategic_project_tracking()
    project_page.right_click_mission_project_tracking()

    # ---------- ADD MILESTONE ----------
    project_page.click_add_milestone_from_context()

    project_page.fill_milestone_details(
    milestone_name=data["milestone_name"],
    start_day=data["start_day"],
    end_day=data["end_day"],
    remarks=data["remarks"],
    file_path=data["file_path"],
)

    project_page.save_milestone()
    project_page.verify_milestone_created(data["milestone_name"])

    AllureHelper.attach_pass_description(tcid)

# =====================================================
# PRJ_06 – ADD TASK FROM TREE
# =====================================================
@pytest.mark.task
def test_prj_06_add_task_from_tree(page: Page):
    tcid = "PRJ_06"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    # ---------- LOGIN ----------
    login_page.open_login()
    login_page.login(data["email"], data["password"])

    # ---------- NAVIGATE ----------
    page.get_by_role("link", name="Projects").click()

    # ---------- TREE FLOW ----------
    project_page.open_project_tree()
    project_page.expand_strategic_project_tracking()
    project_page.expand_mission_project_tracking()

    project_page.right_click_phase_node(
        data["phase_name"]
    )

    # ---------- ADD TASK ----------
    project_page.click_add_task_from_context()

    project_page.fill_task_details(
        task_name=data["task_name"],
        priority=data["priority"],
        complexity=data["complexity"],
        remarks=data["remarks"],
        file_path=data["file_path"],
    )

    project_page.save_task()

    AllureHelper.attach_pass_description(tcid)

    # =====================================================
# PRJ_07 – ADD SUBTASK FROM TREE
# =====================================================
@pytest.mark.subtask
def test_prj_07_add_subtask_from_tree(page: Page):
    tcid = "PRJ_07"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    # ---------- LOGIN ----------
    login_page.open_login()
    login_page.login(data["email"], data["password"])

    # ---------- NAVIGATE ----------
    page.get_by_role("link", name="Projects").click()

    # ---------- TREE FLOW ----------
    project_page.open_project_tree()
    project_page.expand_strategic_project_tracking()
    project_page.expand_mission_project_tracking()
    project_page.expand_phase_node(data["phase_name"])

    project_page.right_click_task_node(
        data["task_name"]
    )

    # ---------- ADD SUBTASK ----------
    project_page.click_add_subtask_from_context()

    project_page.fill_subtask_details(
        subtask_name=data["subtask_name"],
        start_day=data["start_day"],
        end_day=data["end_day"],
        assign_to=data["assign_to"],
        assignee=data["assignee"],
        shift=data["shift"],
        priority=data["priority"],
        complexity=data["complexity"],
        remarks=data["remarks"],
        file_path=data["file_path"],
    )

    project_page.save_subtask()
    AllureHelper.attach_pass_description(tcid)


# =====================================================
# PRJ_08 – ADD WORKLOG FROM TREE
# =====================================================
@pytest.mark.worklog
def test_prj_08_add_worklog_from_tree(page: Page):
    tcid = "PRJ_08"
    AllureHelper.attach_common_description(tcid)

    data = get_test_data(tcid)

    login_page = LoginPage(page)
    project_page = ProjectPage(page)

    # ---------- LOGIN ----------
    login_page.open_login()
    login_page.login(data["email"], data["password"])

    # ---------- NAVIGATE ----------
    page.get_by_role("link", name="Projects").click()

    # ---------- TREE FLOW ----------
    project_page.open_project_tree()
    project_page.expand_strategic_project_tracking()
    project_page.expand_mission_project_tracking()
    project_page.expand_phase_node(data["phase_name"])
    project_page.expand_task_node(data["task_name"])

    project_page.right_click_subtask_node(
        data["subtask_name"]
    )

    # ---------- ADD WORKLOG ----------
    project_page.click_add_worklog_from_context()

    project_page.fill_worklog_details(
        worklog_day=data["worklog_day"],
        time_spent=data["time_spent"],
        work_description=data["work_description"],
        remarks=data["remarks"],
        file_path=data["file_path"],
    )

    project_page.save_worklog()
    AllureHelper.attach_pass_description(tcid)


