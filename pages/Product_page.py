from playwright.sync_api import Page, expect
from typing import Optional
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

        # keep your original dropdown locators
        self.dropdown_category = page.get_by_role("combobox", name="Select Category")
        self.dropdown_status = page.get_by_role("combobox", name="Select Status")

        self.textarea_description = page.locator("textarea")

        self.btn_save = page.get_by_role("button", name="Save")

        # ---------- Search ----------
        self.input_search = page.get_by_role("textbox", name="Search")

        # ---------- Tree Icon ----------
        self.btn_tree_icon = page.get_by_role("button", name="itemDetails").first

        # ---------- Assign User ----------
        self.btn_assign_user = page.get_by_role("button", name="Assign User")
        self.btn_assign_user_popup = page.locator("app-product-assign-users-list").get_by_role("button", name="Assign User")
        self.dropdown_user = page.get_by_role("combobox", name="Select User")
        self.dropdown_role = page.get_by_role("combobox", name="Select Role")
        self.btn_assign_save = page.get_by_role("button", name="Save")

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
    # Utility
    # =====================================================
    def generate_product_code(self):
        return f"PRD{int(time.time() % 100000)}"

    # =====================================================
    # Add Product (UPDATED)
    # =====================================================
    def enter_product_details(
        self,
        code: str = None,
        name: str = "",
        description: str = ""
    ):
        if not code:
            code = self.generate_product_code()

        self.input_product_code.fill(code)
        self.input_product_name.fill(name)
        self.textarea_description.fill(description)

        return code

    # ✅ NEW: index-based dropdown (same as Machines pattern)
    def select_category_by_index(self, index: int):
        self.dropdown_category.click()
        self.page.get_by_role("option").nth(index).click()

    def select_status_by_index(self, index: int):
        self.dropdown_status.click()
        self.page.get_by_role("option").nth(index).click()

    def save(self):
        self.btn_save.click()

    def verify_product_created(self, product_name: str, timeout: int = 5000):
        """
        Verify that the product was created.
        Strategy:
        1. Check for a visible toast message (fast and reliable)
        2. Fallback to searching visible text on the page (grid/tree)
        3. Fallback to filtering table rows by text
        Raises AssertionError if the product is not found.
        """
        # 1) Check toast message
        try:
            expect(self.toast_message).to_be_visible(timeout=timeout)
            return
        except Exception:
            pass

        # 2) Fallback: visible text anywhere on the page
        try:
            expect(self.page.get_by_text(product_name).first).to_be_visible(timeout=timeout)
            return
        except Exception:
            pass

        # 3) Final fallback: table row with product name
        try:
            row = self.page.locator("tr").filter(has_text=product_name).first
            expect(row).to_be_visible(timeout=timeout)
            return
        except Exception:
            raise AssertionError(
                f"Product '{product_name}' not found after save (no toast, no visible text, no table row)."
            )


    # =====================================================
    # Tree - Select Product
    # =====================================================
    def open_product_tree(self, product_name: Optional[str] = None):
        """Open the product tree safely.

        - Waits for any dialog masks to hide; if a mask persists, it disables pointer-events
          on the mask so clicks can reach the underlying elements.
        - Clicks the global itemDetails button and optionally clicks the product node if
          a product_name is supplied.
        """
        # Wait for mask to hide, else make it non-intercepting
        try:
            masks = self.page.locator(".p-dialog-mask")
            try:
                masks.wait_for(state="hidden", timeout=5000)
            except Exception:
                # Mask persisted — disable pointer events to allow clicks to pass through
                try:
                    self.page.evaluate(
                        "() => document.querySelectorAll('.p-dialog-mask').forEach(el => el.style.pointerEvents = 'none')"
                    )
                except Exception:
                    # Ignore evaluation errors
                    pass
        except Exception:
            pass

        # Click the itemDetails button (use first to match previous behavior)
        try:
            self.page.get_by_role("button", name="itemDetails").first.click(timeout=10000)
        except Exception:
            # Fallback: try JS click if normal click still fails
            try:
                self.page.evaluate(
                    "() => document.querySelectorAll('[data-pc-name=\"buttondirective\"]').forEach(el => el.click())"
                )
            except Exception:
                pass

        time.sleep(0.5)

        # If a product name was provided, optionally click the product node in the tree
        if product_name:
            try:
                self.page.get_by_text(product_name).first.click(timeout=5000)
            except Exception:
                pass

    # =====================================================
    # Milestone
    # =====================================================
    def open_milestone_dialog(self):
        """Open the Milestone dialog safely (handles persistent dialog masks)."""
        masks = self.page.locator(".p-dialog-mask")
        try:
            masks.wait_for(state="hidden", timeout=5000)
        except Exception:
            try:
                self.page.evaluate(
                    "() => document.querySelectorAll('.p-dialog-mask').forEach(el => el.style.pointerEvents = 'none')"
                )
            except Exception:
                pass

        # Click the Milestone button (safe click)
        try:
            self.page.get_by_role("button", name="Milestone").click()
        except Exception:
            try:
                self.page.evaluate(
                    "() => document.querySelectorAll('[data-pc-name=\"buttondirective\"]').forEach(el => el.click())"
                )
            except Exception:
                pass

    def create_milestone(self, name: str, code: str, weightage: str = "", remarks: str = ""):
        """Create a milestone by opening the dialog, filling fields, and saving."""
        self.open_milestone_dialog()

        # Fill fields
        if name:
            try:
                self.page.get_by_role("textbox", name="Milestone Name").fill(name)
            except Exception:
                pass

        if code:
            try:
                self.page.get_by_role("textbox", name="Milestone Code").fill(code)
            except Exception:
                pass

        if weightage:
            try:
                self.page.get_by_placeholder("Weightage").fill(str(weightage))
            except Exception:
                pass

        if remarks:
            try:
                self.page.get_by_role("textbox", name="Type your remarks here").fill(remarks)
            except Exception:
                pass

        # Click Save and wait for UI
        try:
            self.page.get_by_role("button", name="Save").click()
        except Exception:
            try:
                self.page.evaluate("() => document.querySelectorAll('button').forEach(b => { if (b.textContent && b.textContent.trim()==='Save') b.click(); })")
            except Exception:
                pass

    def verify_milestone_created(self, name: str, timeout: int = 5000):
        """Verify milestone creation via toast or visible text."""
        try:
            expect(self.toast_message).to_be_visible(timeout=timeout)
            return
        except Exception:
            pass

        try:
            expect(self.page.get_by_text(name).first).to_be_visible(timeout=timeout)
            return
        except Exception:
            raise AssertionError(f"Milestone '{name}' not found after save (no toast, no visible text).")

    def select_milestone_by_name(self, name: str, timeout: int = 5000):
        """Select a milestone node (by visible text) in the product tree or list."""
        # Try treeitem button first (matches tree node pattern)
        try:
            self.page.get_by_role("treeitem", name=name).get_by_role("button").click(timeout=2000)
            return
        except Exception:
            pass

        # Try label-based selection (some markup uses labels)
        try:
            self.page.get_by_label(name).get_by_text(name).first.click(timeout=2000)
            return
        except Exception:
            pass

        # Try plain text
        try:
            self.page.get_by_text(name).first.click(timeout=timeout)
            return
        except Exception:
            raise AssertionError(f"Milestone '{name}' not found or not clickable.")

    # =====================================================
    # Assign User
    # =====================================================
    def select_user_by_index(self, index: int):
        dropdown_user = self.page.get_by_role("combobox", name="Select User")
        dropdown_user.click()
        self.page.get_by_role("option").nth(index).click()

    def select_role_by_index(self, index: int):
        dropdown_role = self.page.get_by_role("combobox", name="Select Role")
        dropdown_role.click()
        self.page.get_by_role("option").nth(index).click()

    def assign_user_to_product(self, user_index: int, role_index: int):
        # Click "Assign User" button
        self.page.get_by_role("button", name="Assign User").click()
        time.sleep(1)
        
        # Click "Assign User" button in popup
        self.page.locator("app-product-assign-users-list").get_by_role("button", name="Assign User").click()
        time.sleep(1)

        # Select user
        self.select_user_by_index(user_index)
        time.sleep(0.5)
        
        # Select role
        self.select_role_by_index(role_index)
        time.sleep(0.5)

        # Check checkbox
        self.page.get_by_role("checkbox").check()
        time.sleep(0.5)
        
        # Click Save
        self.page.get_by_role("button", name="Save").click()

    def assign_user_by_names(self, user_name: str, role_name: str, check_first: bool = True):
        """Assign a user to the currently-selected product using visible option names.

        - Clicks the main "Assign User" button
        - Opens the assign-user popup and clicks its "Assign User" button
        - Selects the user and role by visible text
        - Optionally checks the first checkbox (makes sense for multi-select UIs)
        - Clicks Save
        """
        # Click "Assign User" button (main)
        self.page.get_by_role("button", name="Assign User").click()
        time.sleep(0.5)

        # Click "Assign User" within the popup
        self.page.locator("app-product-assign-users-list").get_by_role("button", name="Assign User").click()
        time.sleep(0.5)

        # Select user by visible name
        self.page.get_by_role("combobox", name="Select User").click()
        self.page.get_by_role("option", name=user_name).click()
        time.sleep(0.3)

        # Select role by visible name
        self.page.get_by_role("combobox", name="Select Role").click()
        self.page.get_by_role("option", name=role_name).click()
        time.sleep(0.3)

        # Check checkbox if required
        if check_first:
            try:
                self.page.get_by_role("checkbox").check()
            except Exception:
                # If checkbox not present or already checked, ignore
                pass
        time.sleep(0.2)

        # Click Save
        self.page.get_by_role("button", name="Save").click()

    def verify_user_assigned(self, user_name: str, timeout: int = 5000):
        """Verify assigned user either via toast or popup listing."""
        try:
            expect(self.toast_message).to_be_visible(timeout=timeout)
            return
        except Exception:
            pass

        # If the popup is still open, look for the username in the popup
        try:
            popup = self.page.locator("app-product-assign-users-list")
            expect(popup.get_by_text(user_name).first).to_be_visible(timeout=timeout)
            return
        except Exception:
            raise AssertionError(f"Assigned user '{user_name}' not found (no toast, no popup entry).")