from playwright.sync_api import Page, expect
import time


class ProductPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------- Navigation ----------
        self.link_products = page.get_by_role("link", name="Products")
        self.btn_product = page.get_by_role("button", name="Product")

        # ---------- Add Product Form ----------
        self.input_product_code = page.get_by_role("textbox", name="Enter Product Code")
        self.input_product_name = page.get_by_role("textbox", name="Enter Product Name")

        self.dropdown_category = page.get_by_role("combobox", name="Select Category")
        self.dropdown_status = page.get_by_role("combobox", name="Select Status")

        self.textarea_description = page.locator("textarea")

        self.btn_save = page.get_by_role("button", name="Save")

        # ---------- Search ----------
        self.input_search = page.get_by_role("textbox", name="Search")

        # ---------- Toast ----------
        self.toast_message = page.locator(
            ".toast-message, .p-toast-detail, .alert-success"
        )

    # =====================================================
    # Navigation
    # =====================================================
    def open_product_screen(self):
        self.link_products.click()
        self.btn_product.click()

    # =====================================================
    # Utility (NEW)
    # =====================================================
    def generate_product_code(self):
        """
        Generates unique product code like PRD12345
        """
        return f"PRD{int(time.time() % 100000)}"

    # =====================================================
    # Add Product
    # =====================================================
    def enter_product_details(
        self,
        code: str = None,
        name: str = "",
        category: str = "",
        status: str = "",
        description: str = ""
    ):
        # ✅ If code not passed, generate dynamically
        if not code:
            code = self.generate_product_code()

        self.input_product_code.fill(code)
        self.input_product_name.fill(name)

        self.dropdown_category.click()
        self.page.get_by_text(category, exact=True).click()

        self.dropdown_status.click()
        self.page.get_by_role("option", name=status).click()

        self.textarea_description.fill(description)

        # return generated code if needed by test
        return code

    def save(self):
        self.btn_save.click()

    def verify_product_created(self, product_name: str):
        try:
            expect(self.toast_message).to_be_visible(timeout=5000)
        except Exception:
            expect(
                self.page.get_by_text(product_name).first
            ).to_be_visible(timeout=5000)

    # =====================================================
    # Search Product
    # =====================================================
    def search_product(self, text: str):
        self.input_search.click()
        self.input_search.fill(text)

    def verify_search_result(self, text: str):
        expect(
            self.page.get_by_text(text).first
        ).to_be_visible(timeout=5000)

    # =====================================================
    # Update Product
    # =====================================================
    def click_edit_first_product(self):
        self.page.get_by_role("button").nth(1).click()

    def update_product_name(self, new_name: str):
        self.input_product_name.click()
        self.input_product_name.fill(new_name)

    def update_description(self, description: str):
        self.textarea_description.click()
        self.textarea_description.fill(description)

    def save_updated_product(self):
        self.btn_save.click()

    def verify_product_updated(self, updated_text: str):
        expect(
            self.page.get_by_text(updated_text).first
        ).to_be_visible(timeout=5000)

    # =====================================================
    # Delete Product
    # =====================================================
    def delete_first_product(self):
        self.page.get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="Yes").click()

    def verify_product_deleted(self, text: str):
        expect(
            self.page.get_by_text(text)
        ).to_have_count(0)
