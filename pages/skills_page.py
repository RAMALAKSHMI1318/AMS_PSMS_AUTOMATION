from playwright.sync_api import Page, expect


class SkillsPage:
  

    def __init__(self, page: Page):
        self.page = page


        self.tab_skills = page.get_by_role("tab", name="Skills")
        self.btn_add_skill = page.get_by_role("button", name="Add Skill")


        self.input_skill_code = page.get_by_role("textbox").nth(1)
        self.input_skill_name = page.get_by_role("textbox").nth(2)
        self.textarea_description = page.locator("textarea")
        self.tab_machines = page.get_by_role("tab", name="Machines")

        self.btn_save = page.get_by_role("button", name="Save")

   
    def open_skills_tab(self):
        self.tab_skills.click()
        
    def open_machines_tab(self):
        self.tab_machines.click()

    def open_add_skill(self):
        self.tab_skills.click()
        self.btn_add_skill.click()

    def enter_skill_details(self, code: str, name: str, description: str):
        self.input_skill_code.fill(code)
        self.input_skill_name.fill(name)
        self.textarea_description.fill(description)

    def save_skill(self):
        self.btn_save.click()

    def verify_skill_created(self):

        toast = (
            self.page
            .locator(".p-toast-detail", has_text="success")
            .first
        )

        expect(toast).to_be_visible(timeout=5000)

    def search_skill(self, search_text: str):
        search_box = self.page.get_by_role(
            "textbox", name="Search Skills"
        )
        search_box.click()
        search_box.fill(search_text)

    
    def verify_skill_search_result(self):
    
        rows = self.page.get_by_role("row")

        expect(rows.first).to_be_visible(timeout=5000)

        if rows.count() <= 1:
            raise AssertionError("No skill records found after search")
        
    def click_edit_first_skill(self):
        self.page.get_by_role("button").nth(1).click()

    def update_skill_code(self, append_value: str):
        code_input = self.page.get_by_role("textbox").nth(1)
        existing_code = code_input.input_value()
        code_input.fill(f"{existing_code}{append_value}")

    def update_skill_name(self, append_value: str):
        name_input = self.page.get_by_role("textbox").nth(2)
        existing_name = name_input.input_value()
        name_input.fill(f"{existing_name}{append_value}")

    def save_updated_skill(self):
        self.page.get_by_role("button", name="Save").click()

    def verify_skill_updated(self):
        toast = (
            self.page
            .locator(".p-toast-detail", has_text="success")
            .first
        )
        expect(toast).to_be_visible(timeout=7000)


        self.tab_skills.click()
    
    def delete_first_skill(self):
        self.page.get_by_role("button").nth(2).click()

        self.page.get_by_role("button", name="Yes").click()

    def verify_skill_deleted(self):
    
        success_msg = (
            self.page
            .get_by_text("Skill deleted successfully")
            .first
        )

        expect(success_msg).to_be_visible(timeout=7000)