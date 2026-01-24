import re
import time
from playwright.sync_api import Page
from base.base_page import BasePage


class DocumentCategoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # ======================
        # NAVIGATION
        # ======================
        self.user_management_link = page.get_by_role(
            "link", name="User Management"
        )
        self.document_categories_tab = page.get_by_role(
            "tab", name="Document Categories"
        )

        # ======================
        # SEARCH
        # ======================
        self.search_box = page.get_by_role(
            "textbox", name="Search"
        )

        # ======================
        # ACTION BUTTONS
        # ======================
        self.add_new_btn = page.get_by_role(
            "button", name="Add New"
        )
        self.save_btn = page.get_by_role(
            "button", name="Save"
        )

        # ======================
        # FORM FIELDS
        # ======================
        self.name_input = page.locator(
            "div"
        ).filter(
            has_text=re.compile(r"^Name \*$")
        ).get_by_role("textbox")

        self.code_input = page.locator(
            "div"
        ).filter(
            has_text=re.compile(r"^Code \*$")
        ).get_by_role("textbox")

        self.description_textarea = page.locator("textarea")

        self.category_type_select = page.locator(
            'select[formcontrolname="category_type"]'
        )

        self.parent_category_input = page.locator(
            'input[formcontrolname="parent_category_id"]'
        )

        self.display_order_input = page.locator(
            'input[formcontrolname="display_order"]'
        )

    # ======================
    # NAVIGATION
    # ======================
    def open_document_categories(self):
        self.user_management_link.wait_for(state="visible", timeout=15000)
        self.user_management_link.click()

        self.document_categories_tab.wait_for(state="visible", timeout=15000)
        self.document_categories_tab.click()

        self.add_new_btn.wait_for(state="visible", timeout=15000)

    # ======================
    # SEARCH
    # ======================
    def search_document_category(self, text: str):
        self.search_box.fill(text.strip())
        time.sleep(1)  # allow table to refresh

    # ======================
    # ADD
    # ======================
    def click_add_new(self):
        self.add_new_btn.click()
        self.name_input.wait_for(state="visible", timeout=10000)

    def fill_name(self, name: str):
        self.name_input.fill(name)
        self.name_input.press("Tab")

    def fill_code(self, code: str):
        self.code_input.fill(code)
        self.code_input.press("Tab")

    def select_category_type(self, value: str):
        self.category_type_select.select_option(value)

    def select_parent_category(self, value: str):
        self.parent_category_input.fill(str(value))

    def fill_display_order(self, order: str):
        self.display_order_input.fill(str(order))

    def fill_description(self, text: str):
        self.description_textarea.fill(text)
        time.sleep(1)

    def click_save(self):
        self.save_btn.click()
        time.sleep(1)

    # ==================================================
    # ✅ EDIT DOCUMENT CATEGORY (BASED ON SEARCH)
    # ==================================================
    def click_edit_by_search(self, search_text: str):
        """
        Search a document category and click Edit icon
        for the matching row
        """
        self.search_document_category(search_text)

        self.page.get_by_role(
            "row",
            name=re.compile(search_text, re.IGNORECASE)
        ).get_by_role("button").first.click()

        # wait for edit dialog
        self.name_input.wait_for(state="visible", timeout=10000)
    # ==================================================
    # ✅ DELETE DOCUMENT CATEGORY (BASED ON SEARCH)
    # ==================================================
    def click_delete_by_search(self, search_text: str):
        """
        Search a document category and delete the matching rowa
        """
        # 1️⃣ Search first
        self.search_document_category(search_text)

        rows = self.page.get_by_role(
            "row",
            name=re.compile(search_text, re.IGNORECASE)
        )

        # 2️⃣ Fail fast if no row found
        if rows.count() == 0:
            raise Exception(
                f"No document category found for delete search: {search_text}"
            )

        # 3️⃣ Click DELETE button (based on recorder: nth(1))
        rows.first.get_by_role("button").nth(1).click()

        # 4️⃣ Confirm delete (Yes button)
        confirm_btn = self.page.get_by_role("button", name="Yes")
        confirm_btn.wait_for(state="visible", timeout=5000)
        confirm_btn.click()

        # 5️⃣ Wait for API & table refresh
        time.sleep(1)
