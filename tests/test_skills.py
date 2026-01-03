import random
import time
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.skills_page import SkillsPage
from utils.allure_helper import AllureHelper


def test_skill01_add_skill(page: Page):
    tcid = "TC_Skill1"

   
    AllureHelper.attach_common_description(tcid)

   
    row = AllureHelper.get_test_row(tcid)

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    description = data_map.get("description")

    
    timestamp = int(time.time())
    skill_code = f"SK{random.randint(1000, 9999)}"
    skill_name = f"Skill_{timestamp}"

    login_page = LoginPage(page)
    skills_page = SkillsPage(page)

    try:
        login_page.open_login()
        login_page.login(email, password)

        
        skills_page.open_machines_tab()
        skills_page.open_add_skill()

      
        skills_page.enter_skill_details(
            code=skill_code,
            name=skill_name,
            description=description
        )
        skills_page.save_skill()
        skills_page.verify_skill_created()
        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
       
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_skill02_search_skill(page: Page):

    tcid = "TC_Skill2"

    AllureHelper.attach_common_description(tcid)

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
    skills_page = SkillsPage(page)

    try:
       
        login_page.open_login()
        login_page.login(email, password)

       
        skills_page.open_machines_tab()
        skills_page.open_skills_tab()
     
        skills_page.search_skill(search_text)

        skills_page.verify_skill_search_result()

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_skill03_update_skill(page: Page):

    tcid = "TC_Skill3"
    AllureHelper.attach_common_description(tcid)

    row = AllureHelper.get_test_row(tcid)

    data_map = {}
    for item in row["Test Data"].split(","):
        if ":" in item:
            key, val = item.split(":", 1)
            data_map[key.strip().lower()] = val.strip()

    email = data_map.get("email")
    password = data_map.get("password")
    search_text = data_map.get("search")
    skill_name_append = data_map.get("skill_name")
    skill_code_append = data_map.get("skill_code")

    login_page = LoginPage(page)
    skills_page = SkillsPage(page)

    try:
        
        login_page.open_login()
        login_page.login(email, password)

      
        skills_page.open_machines_tab()
        skills_page.open_skills_tab()
        skills_page.search_skill(search_text)
        skills_page.click_edit_first_skill()
        skills_page.update_skill_code(skill_code_append)
        skills_page.update_skill_name(skill_name_append)
        skills_page.save_updated_skill()
        skills_page.verify_skill_updated()
        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise

def test_skill04_delete_skill(page: Page):
    tcid = "TC_Skill4"
    AllureHelper.attach_common_description(tcid)
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
    skills_page = SkillsPage(page)
    try:
        login_page.open_login()
        login_page.login(email, password)
        skills_page.open_machines_tab()
        skills_page.open_skills_tab()
        skills_page.search_skill(search_text)
        skills_page.delete_first_skill()
        skills_page.verify_skill_deleted()

        AllureHelper.attach_pass_description(tcid)

    except Exception as e:
        
        AllureHelper.attach_fail_description(tcid)
        AllureHelper.attach_failure(str(e))
        raise
